# database_manager.py
import os
import subprocess
import json
import re
from datetime import datetime
from typing import List, Dict, Optional
import threading
import time

class DatabaseManager:
    """Gerenciador do banco de dados local do MSFVenom"""
    
    def __init__(self, db_path="database"):
        self.db_path = db_path
        self.cache = {}
        self.lock = threading.Lock()
        self._ensure_db_path()
        
    def _ensure_db_path(self):
        """Garante que o diretório do banco de dados existe"""
        if not os.path.exists(self.db_path):
            os.makedirs(self.db_path)
    
    def _get_file_path(self, name: str) -> str:
        """Retorna o caminho completo do arquivo"""
        return os.path.join(self.db_path, f"{name}.txt")
    
    def _get_json_path(self, name: str) -> str:
        """Retorna o caminho do arquivo JSON"""
        return os.path.join(self.db_path, f"{name}.json")
    
    def _run_msfvenom_command(self, command: str) -> str:
        """Executa comando msfvenom e retorna a saída"""
        try:
            cmd = ['msfvenom', '-l', command]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                raise Exception(f"Erro ao executar msfvenom -l {command}: {result.stderr}")
            
            return result.stdout
            
        except subprocess.TimeoutExpired:
            raise Exception(f"Timeout ao executar msfvenom -l {command}")
        except Exception as e:
            raise Exception(f"Erro ao executar msfvenom -l {command}: {str(e)}")
    
    def _parse_list_output(self, output: str) -> List[str]:
        """Parseia a saída do msfvenom -l"""
        lines = output.split('\n')
        items = []
        in_table = False
        
        for line in lines:
            if '========' in line or '----' in line:
                in_table = True
                continue
            if in_table and line.strip():
                parts = line.split()
                if parts and parts[0] not in ['Name', '----']:
                    if len(parts[0]) > 1:
                        items.append(parts[0])
        
        if not items:
            for line in lines:
                line = line.strip()
                if line and '/' in line and not line.startswith('='):
                    parts = line.split()
                    if parts and len(parts[0]) > 1:
                        items.append(parts[0])
        
        return items
    
    def get_or_create_list(self, command: str, force_update: bool = False) -> List[str]:
        """Obtém lista do cache ou cria novo arquivo"""
        with self.lock:
            file_path = self._get_file_path(command)
            json_path = self._get_json_path(command)
            
            if not force_update and os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                try:
                    if os.path.exists(json_path):
                        with open(json_path, 'r', encoding='utf-8') as f:
                            return json.load(f)
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        items = self._parse_list_output(content)
                        
                    with open(json_path, 'w', encoding='utf-8') as f:
                        json.dump(items, f, indent=2, ensure_ascii=False)
                    
                    return items
                except Exception as e:
                    print(f"⚠️ Erro ao ler {command}.txt: {str(e)}")
            
            try:
                print(f"📥 Gerando {command}.txt...")
                output = self._run_msfvenom_command(command)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(output)
                
                items = self._parse_list_output(output)
                
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(items, f, indent=2, ensure_ascii=False)
                
                return items
                
            except Exception as e:
                print(f"❌ Erro ao gerar {command}.txt: {str(e)}")
                return self._get_fallback_list(command)
    
    def _get_fallback_list(self, command: str) -> List[str]:
        """Retorna lista de fallback"""
        fallbacks = {
            'payloads': [
                'windows/meterpreter/reverse_tcp',
                'windows/meterpreter/reverse_https',
                'windows/meterpreter/reverse_http',
                'windows/meterpreter/bind_tcp',
                'windows/shell/reverse_tcp',
                'windows/shell/bind_tcp',
                'windows/exec',
                'windows/x64/meterpreter/reverse_tcp',
                'windows/x64/shell/reverse_tcp',
                'windows/x64/exec',
                'linux/x86/meterpreter/reverse_tcp',
                'linux/x86/shell/reverse_tcp',
                'linux/x86/exec',
                'linux/x64/meterpreter/reverse_tcp',
                'linux/x64/shell/reverse_tcp',
                'linux/x64/exec',
                'android/meterpreter/reverse_tcp',
                'android/meterpreter/reverse_https',
                'android/meterpreter/bind_tcp',
                'android/shell/reverse_tcp',
                'android/exec',
                'java/meterpreter/reverse_tcp',
                'java/meterpreter/reverse_https',
                'java/meterpreter/bind_tcp',
                'java/shell/reverse_tcp',
                'php/meterpreter_reverse_tcp',
                'php/meterpreter_bind_tcp',
                'php/shell_reverse_tcp',
                'python/meterpreter/reverse_tcp',
                'python/meterpreter/reverse_https',
                'python/meterpreter/bind_tcp',
                'python/shell_reverse_tcp',
                'osx/x64/meterpreter/reverse_tcp',
                'osx/x64/shell_reverse_tcp',
                'osx/x64/exec',
            ],
            'exploits': [
                'exploit/multi/handler',
                'exploit/windows/smb/ms17_010_eternalblue',
                'exploit/windows/local/ms16_014',
                'exploit/windows/smb/ms08_067_netapi',
                'exploit/linux/smb/ms17_010_psexec',
                'exploit/linux/local/pkexec',
            ],
            'encoders': [
                'x86/shikata_ga_nai',
                'x86/jmp_call_additive',
                'x86/alpha_mixed',
                'x86/alpha_upper',
                'x64/xor',
                'x64/xor_dynamic',
                'x64/zutto_dekiru',
                'cmd/powershell_base64',
                'cmd/printf_php_mq',
                'generic/none',
            ],
            'formats': [
                'exe', 'elf', 'apk', 'py', 'php', 'raw', 'c', 'ruby',
                'perl', 'ps1', 'vba', 'vbs', 'hex', 'jar', 'class',
                'war', 'asp', 'aspx', 'jsp', 'jspx', 'pl', 'pm',
                'rb', 'sh', 'bash', 'zsh', 'fish', 'cmd', 'bat',
                'ps1', 'psm1', 'psd1', 'psrc', 'xml', 'yaml',
                'json', 'csv', 'tsv', 'html', 'htm', 'js',
                'dll', 'so', 'dylib', 'sys', 'bin', 'dat'
            ],
            'platforms': [
                'windows', 'linux', 'android', 'java', 'php', 'python',
                'osx', 'macos', 'solaris', 'bsd', 'aix', 'hpux',
                'irix', 'netware', 'openbsd', 'freebsd', 'netbsd',
                'sunos', 'unix', 'generic', 'cisco', 'ios',
                'ruby', 'nodejs', 'cmd',
            ],
            'archs': [
                'x86', 'x64', 'armle', 'aarch64', 'dalvik', 'sparc',
                'ppc', 'ppc64', 'mips', 'mipsbe', 'mipsle', 'mips64',
                'ia64', 'alpha', 'parisc', 's390', 's390x', 'hppa',
                'sh4', 'c67x', 'm68k', 'z80', 'java', 'ruby', 'php',
                'python', 'nodejs', 'cmd', 'all',
            ]
        }
        
        return fallbacks.get(command, [])
    
    def get_payload_options(self, payload_name: str, force_update: bool = False) -> Dict:
        """Obtém opções de um payload específico"""
        cache_key = f"payload_{payload_name}"
        if not force_update and cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            print(f"🔍 Obtendo opções de {payload_name}...")
            cmd = ['msfvenom', '-p', payload_name, '--list-options']
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                return {'error': f'Erro ao obter opções: {result.stderr}'}
            
            options = self._parse_options_output(result.stdout, payload_name)
            
            # Adicionar opções específicas para certos payloads
            options = self._add_specific_options(payload_name, options)
            
            self.cache[cache_key] = options
            return options
            
        except subprocess.TimeoutExpired:
            # Se timeout, tentar usar opções conhecidas
            return self._get_known_options(payload_name)
        except Exception as e:
            return {'error': str(e)}
    
    def _add_specific_options(self, payload_name: str, options: Dict) -> Dict:
        """Adiciona opções específicas para payloads conhecidos"""
        
        # Android específico
        if 'android' in payload_name.lower():
            android_options = [
                {'name': 'AndroidHideAppIcon', 'current_setting': 'false', 'required': 'no', 
                 'description': 'Hide the application icon automatically after launch'},
                {'name': 'AutoRunScript', 'current_setting': '', 'required': 'no', 
                 'description': 'A script to run automatically on session creation'},
                {'name': 'AutoVerifySession', 'current_setting': 'true', 'required': 'no', 
                 'description': 'Automatically verify and setup the session'},
                {'name': 'InitialAutoRunScript', 'current_setting': '', 'required': 'no', 
                 'description': 'Initial script to run before session creation'},
                {'name': 'EnableStageEncoding', 'current_setting': 'false', 'required': 'no', 
                 'description': 'Enable stage encoding'},
                {'name': 'StageEncoder', 'current_setting': '', 'required': 'no', 
                 'description': 'Encoder to use for stage encoding'},
                {'name': 'StageEncoderSaveRegisters', 'current_setting': '', 'required': 'no', 
                 'description': 'Save registers for stage encoder'},
            ]
            
            if not options.get('basic_options'):
                options['basic_options'] = []
            
            # Adicionar opções do Android que não existem
            existing_names = [opt['name'] for opt in options['basic_options']]
            for opt in android_options:
                if opt['name'] not in existing_names:
                    options['basic_options'].append(opt)
            
            # Atualizar required options
            if 'required_options' not in options:
                options['required_options'] = []
        
        # Meterpreter específico
        if 'meterpreter' in payload_name.lower():
            meterpreter_options = [
                {'name': 'AutoLoadExtensions', 'current_setting': 'unhook,priv,stdapi', 'required': 'yes', 
                 'description': 'Automatically load extensions on bootstrap, comma separated'},
                {'name': 'AutoUnhookProcess', 'current_setting': 'true', 'required': 'no', 
                 'description': 'Automatically unhook the process'},
                {'name': 'EnableStageEncoding', 'current_setting': 'false', 'required': 'no', 
                 'description': 'Enable stage encoding'},
                {'name': 'InitialAutoRunScript', 'current_setting': '', 'required': 'no', 
                 'description': 'Initial script to run before session creation'},
                {'name': 'AutoVerifySession', 'current_setting': 'true', 'required': 'no', 
                 'description': 'Automatically verify and setup the session'},
            ]
            
            if not options.get('basic_options'):
                options['basic_options'] = []
            
            existing_names = [opt['name'] for opt in options['basic_options']]
            for opt in meterpreter_options:
                if opt['name'] not in existing_names:
                    options['basic_options'].append(opt)
        
        # Windows específico
        if 'windows' in payload_name.lower():
            windows_options = [
                {'name': 'EXITFUNC', 'current_setting': 'process', 'required': 'yes', 
                 'description': 'Exit function (process, thread, seh)'},
                {'name': 'VERBOSE', 'current_setting': 'false', 'required': 'no', 
                 'description': 'Enable verbose output'},
                {'name': 'AutoRunScript', 'current_setting': '', 'required': 'no', 
                 'description': 'Script to run on session creation'},
                {'name': 'AutoVerifySession', 'current_setting': 'true', 'required': 'no', 
                 'description': 'Automatically verify and setup the session'},
            ]
            
            if not options.get('basic_options'):
                options['basic_options'] = []
            
            existing_names = [opt['name'] for opt in options['basic_options']]
            for opt in windows_options:
                if opt['name'] not in existing_names:
                    options['basic_options'].append(opt)
        
        return options
    
    def _get_known_options(self, payload_name: str) -> Dict:
        """Retorna opções conhecidas para payloads específicos"""
        info = {
            'name': payload_name,
            'description': f'Payload: {payload_name}',
            'basic_options': [],
            'advanced_options': [],
            'evasion_options': [],
            'required_options': [],
            'all_options': {}
        }
        
        # LHOST e LPORT são comuns
        if 'reverse' in payload_name.lower() or 'meterpreter' in payload_name.lower():
            info['basic_options'] = [
                {'name': 'LHOST', 'current_setting': '', 'required': 'yes', 'description': 'The local host to connect back to'},
                {'name': 'LPORT', 'current_setting': '4444', 'required': 'yes', 'description': 'The local port to connect back to'},
            ]
            info['required_options'] = ['LHOST', 'LPORT']
        
        if 'bind' in payload_name.lower():
            info['basic_options'] = [
                {'name': 'RHOST', 'current_setting': '', 'required': 'yes', 'description': 'The target host to bind to'},
                {'name': 'RPORT', 'current_setting': '4444', 'required': 'yes', 'description': 'The port to bind on'},
            ]
            info['required_options'] = ['RHOST', 'RPORT']
        
        # Adicionar opções específicas
        info = self._add_specific_options(payload_name, info)
        
        return info
    
    def _parse_options_output(self, output: str, name: str) -> Dict:
        """Parseia a saída do --list-options"""
        info = {
            'name': name,
            'description': '',
            'basic_options': [],
            'advanced_options': [],
            'evasion_options': [],
            'required_options': [],
            'all_options': {}
        }
        
        lines = output.split('\n')
        current_section = None
        description_lines = []
        
        for line in lines:
            line_clean = line.strip()
            
            if 'Description:' in line:
                current_section = 'description'
                desc = line.replace('Description:', '').strip()
                if desc:
                    description_lines.append(desc)
                continue
            
            elif 'Basic options:' in line:
                current_section = 'basic'
                continue
            
            elif 'Advanced options:' in line:
                current_section = 'advanced'
                continue
            
            elif 'Evasion options:' in line:
                current_section = 'evasion'
                continue
            
            elif current_section == 'description' and line_clean:
                if not line_clean.startswith('----') and not line_clean.startswith('==='):
                    description_lines.append(line_clean)
            
            elif current_section in ['basic', 'advanced', 'evasion'] and line_clean:
                if line_clean.startswith('----') or 'Name' in line_clean:
                    continue
                
                option_data = self._parse_option_line(line_clean)
                if option_data:
                    if current_section == 'basic':
                        info['basic_options'].append(option_data)
                    elif current_section == 'advanced':
                        info['advanced_options'].append(option_data)
                    elif current_section == 'evasion':
                        info['evasion_options'].append(option_data)
                    
                    info['all_options'][option_data['name']] = option_data
                    
                    if option_data.get('required', '').lower() == 'yes':
                        info['required_options'].append(option_data['name'])
        
        if description_lines:
            info['description'] = ' '.join(description_lines)
        
        return info
    
    def _parse_option_line(self, line: str) -> Dict:
        """Parseia uma linha de opção"""
        line = line.strip()
        if not line:
            return None
        
        parts = re.split(r'\s{2,}', line)
        
        if len(parts) < 2:
            return None
        
        name = parts[0].strip()
        required = 'no'
        description = ''
        current_setting = ''
        
        # Procurar por 'yes' ou 'no'
        for i, part in enumerate(parts):
            if part.lower() in ['yes', 'no']:
                required = part.lower()
                if i + 1 < len(parts):
                    description = ' '.join(parts[i+1:])
                break
        
        if required == 'no' and len(parts) >= 3:
            for i, part in enumerate(parts):
                if part.lower() in ['yes', 'no']:
                    required = part.lower()
                    if i + 1 < len(parts):
                        description = ' '.join(parts[i+1:])
                    break
        
        if not description and len(parts) > 1:
            description = parts[-1]
            if len(parts) > 2 and parts[-2].lower() in ['yes', 'no']:
                required = parts[-2].lower()
                description = parts[-1]
        
        return {
            'name': name,
            'current_setting': current_setting,
            'required': required,
            'description': description,
            'type': 'string'
        }
    
    def get_exploit_options(self, exploit_name: str) -> Dict:
        """Obtém opções de um exploit específico"""
        try:
            cmd = ['msfvenom', '-e', exploit_name, '--list-options']
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=20
            )
            
            if result.returncode == 0:
                options = self._parse_options_output(result.stdout, exploit_name)
                return options
            
        except:
            pass
        
        # Fallback para exploits conhecidos
        info = {
            'name': exploit_name,
            'description': f'Exploit: {exploit_name}',
            'basic_options': [],
            'advanced_options': [],
            'required_options': [],
            'all_options': {}
        }
        
        if 'eternalblue' in exploit_name.lower():
            info['basic_options'] = [
                {'name': 'RHOSTS', 'current_setting': '', 'required': 'yes', 'description': 'Target host(s)'},
                {'name': 'RPORT', 'current_setting': '445', 'required': 'yes', 'description': 'Target port'},
                {'name': 'SMBUser', 'current_setting': '', 'required': 'no', 'description': 'SMB Username'},
                {'name': 'SMBPass', 'current_setting': '', 'required': 'no', 'description': 'SMB Password'},
                {'name': 'VERBOSE', 'current_setting': 'false', 'required': 'no', 'description': 'Enable verbose output'},
            ]
            info['required_options'] = ['RHOSTS', 'RPORT']
            
        elif 'handler' in exploit_name.lower():
            info['basic_options'] = [
                {'name': 'PAYLOAD', 'current_setting': '', 'required': 'yes', 'description': 'Payload to use'},
                {'name': 'LHOST', 'current_setting': '', 'required': 'yes', 'description': 'Local host'},
                {'name': 'LPORT', 'current_setting': '4444', 'required': 'yes', 'description': 'Local port'},
                {'name': 'EXITFUNC', 'current_setting': 'process', 'required': 'yes', 'description': 'Exit function'},
            ]
            info['required_options'] = ['PAYLOAD', 'LHOST', 'LPORT']
            
        elif 'pkexec' in exploit_name.lower():
            info['basic_options'] = [
                {'name': 'SESSION', 'current_setting': '', 'required': 'yes', 'description': 'Session to exploit'},
                {'name': 'LHOST', 'current_setting': '', 'required': 'yes', 'description': 'Local host'},
                {'name': 'LPORT', 'current_setting': '4444', 'required': 'yes', 'description': 'Local port'},
                {'name': 'VERBOSE', 'current_setting': 'false', 'required': 'no', 'description': 'Enable verbose output'},
            ]
            info['required_options'] = ['SESSION', 'LHOST']
            
        elif 'struts' in exploit_name.lower():
            info['basic_options'] = [
                {'name': 'RHOSTS', 'current_setting': '', 'required': 'yes', 'description': 'Target host(s)'},
                {'name': 'RPORT', 'current_setting': '8080', 'required': 'yes', 'description': 'Target port'},
                {'name': 'TARGETURI', 'current_setting': '/', 'required': 'no', 'description': 'Target URI'},
                {'name': 'PAYLOAD', 'current_setting': '', 'required': 'yes', 'description': 'Payload to use'},
            ]
            info['required_options'] = ['RHOSTS', 'RPORT']
        
        return info
    
    def get_encoder_options(self, encoder_name: str) -> Dict:
        """Obtém opções de um encoder específico"""
        info = {
            'name': encoder_name,
            'description': f'Encoder: {encoder_name}',
            'basic_options': [],
            'advanced_options': [],
            'required_options': [],
            'all_options': {}
        }
        
        # Opções comuns para encoders
        info['basic_options'] = [
            {'name': 'Verbose', 'current_setting': 'false', 'required': 'no', 'description': 'Enable verbose output'},
            {'name': 'ForceEncode', 'current_setting': 'false', 'required': 'no', 'description': 'Force encoding even if not needed'},
        ]
        
        # Opções específicas para shikata_ga_nai
        if 'shikata' in encoder_name.lower():
            info['basic_options'].extend([
                {'name': 'BufferRegister', 'current_setting': '', 'required': 'no', 'description': 'Register to use for buffer'},
                {'name': 'XorCount', 'current_setting': '1', 'required': 'no', 'description': 'Number of XOR operations'},
            ])
        
        return info
    
    def get_all_lists(self, force_update: bool = False) -> Dict:
        """Obtém todas as listas necessárias"""
        lists = {}
        commands = ['payloads', 'exploits', 'encoders', 'formats', 'platforms', 'archs']
        
        for cmd in commands:
            try:
                lists[cmd] = self.get_or_create_list(cmd, force_update)
            except Exception as e:
                print(f"❌ Erro ao carregar {cmd}: {str(e)}")
                lists[cmd] = self._get_fallback_list(cmd)
        
        return lists
    
    def get_item_info(self, item_type: str, item_name: str, force_update: bool = False) -> Dict:
        """Obtém informações de um item específico"""
        if item_type == 'payloads':
            return self.get_payload_options(item_name, force_update)
        elif item_type == 'exploits':
            return self.get_exploit_options(item_name)
        elif item_type == 'encoders':
            return self.get_encoder_options(item_name)
        else:
            return {'error': f'Tipo não suportado: {item_type}'}
    
    def clear_cache(self):
        """Limpa o cache"""
        self.cache.clear()
    
    def get_database_info(self) -> Dict:
        """Obtém informações sobre o database"""
        info = {
            'path': self.db_path,
            'files': [],
            'total_size': 0,
            'last_updated': None
        }
        
        if os.path.exists(self.db_path):
            for file in os.listdir(self.db_path):
                if file.endswith('.txt') or file.endswith('.json'):
                    file_path = os.path.join(self.db_path, file)
                    size = os.path.getsize(file_path)
                    mtime = os.path.getmtime(file_path)
                    info['files'].append({
                        'name': file,
                        'size': size,
                        'modified': datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
                    })
                    info['total_size'] += size
        
        return info

# Singleton para uso global
db_manager = DatabaseManager()
