import os
import subprocess
import re

class DiskpartEmulator:
    def __init__(self):
        self.running = True
        self.selected_disk = None
        self.selected_partition = None
        self.disks = self.get_disks_info()
        
    def get_disks_info(self):
        """Получение информации о дисках через wmic"""
        try:
            result = subprocess.run(
                ['wmic', 'diskdrive', 'list', 'brief'],
                capture_output=True,
                text=True,
                shell=True
            )
            return result.stdout
        except Exception as e:
            return f"Ошибка получения информации о дисках: {e}"
    
    def list_disks(self):
        """Имитация команды LIST DISK"""
        print("\n--- Доступные диски ---")
        print(self.disks)
        print("------------------------\n")
    
    def select_disk(self, disk_number):
        """Имитация команды SELECT DISK"""
        try:
            self.selected_disk = int(disk_number)
            print(f"\nДиск {self.selected_disk} выбран.\n")
        except ValueError:
            print("\nОшибка: Неверный номер диска\n")
    
    def list_partitions(self):
        """Имитация команды LIST PARTITION"""
        if self.selected_disk is None:
            print("\nСначала выберите диск (SELECT DISK X)\n")
            return
        
        print(f"\n--- Разделы на диске {self.selected_disk} ---")
        # Здесь можно добавить реальное получение информации о разделах
        print("Раздел 1 - Основной - 100 ГБ")
        print("Раздел 2 - Системный - 50 ГБ")
        print("------------------------------------\n")
    
    def clean_disk(self):
        """Имитация команды CLEAN"""
        if self.selected_disk is None:
            print("\nСначала выберите диск\n")
            return
        
        confirm = input(f"Вы уверены, что хотите очистить диск {self.selected_disk}? (yes/no): ")
        if confirm.lower() == 'yes':
            print(f"\nДиск {self.selected_disk} очищен.\n")
        else:
            print("\nОперация отменена.\n")
    
    def create_partition(self, size=None):
        """Имитация команды CREATE PARTITION"""
        if self.selected_disk is None:
            print("\nСначала выберите диск\n")
            return
        
        if size:
            print(f"\nСоздан раздел размером {size} МБ на диске {self.selected_disk}\n")
        else:
            print(f"\nСоздан основной раздел на диске {self.selected_disk}\n")
    
    def format_partition(self, filesystem="NTFS", label=""):
        """Имитация команды FORMAT"""
        if self.selected_disk is None:
            print("\nСначала выберите диск\n")
            return
        
        print(f"\nФорматирование раздела в {filesystem}...")
        if label:
            print(f"Метка тома: {label}")
        print("Форматирование завершено.\n")
    
    def assign_letter(self, letter):
        """Имитация команды ASSIGN"""
        if self.selected_disk is None:
            print("\nСначала выберите диск\n")
            return
        
        print(f"\nТому назначена буква {letter.upper()}:\n")
    
    def exit_program(self):
        """Выход из программы"""
        self.running = False
        print("\nВыход из DISKPART...\n")
    
    def show_help(self):
        """Показать доступные команды"""
        print("\n--- Доступные команды ---")
        print("LIST DISK           - показать список дисков")
        print("SELECT DISK X       - выбрать диск X")
        print("LIST PARTITION      - показать разделы выбранного диска")
        print("CLEAN               - очистить выбранный диск")
        print("CREATE PARTITION    - создать раздел")
        print("CREATE PARTITION SIZE=X - создать раздел размером X МБ")
        print("FORMAT FS=NTFS      - форматировать в NTFS")
        print("FORMAT FS=FAT32     - форматировать в FAT32")
        print("ASSIGN LETTER=X     - назначить букву диска")
        print("HELP                - показать справку")
        print("EXIT                - выйти из программы")
        print("--------------------------\n")
    
    def parse_command(self, command):
        """Парсинг введенной команды"""
        command = command.strip().upper()
        
        if command == "LIST DISK":
            self.list_disks()
        elif command == "LIST PARTITION":
            self.list_partitions()
        elif command.startswith("SELECT DISK"):
            parts = command.split()
            if len(parts) >= 3:
                self.select_disk(parts[2])
            else:
                print("\nИспользование: SELECT DISK X\n")
        elif command == "CLEAN":
            self.clean_disk()
        elif command.startswith("CREATE PARTITION"):
            if "SIZE=" in command:
                size_match = re.search(r'SIZE=(\d+)', command)
                if size_match:
                    self.create_partition(size_match.group(1))
                else:
                    print("\nНеверный формат. Используйте: CREATE PARTITION SIZE=1000\n")
            else:
                self.create_partition()
        elif command.startswith("FORMAT"):
            if "FS=NTFS" in command:
                self.format_partition("NTFS")
            elif "FS=FAT32" in command:
                self.format_partition("FAT32")
            else:
                self.format_partition()
        elif command.startswith("ASSIGN"):
            letter_match = re.search(r'LETTER=([A-Za-z])', command)
            if letter_match:
                self.assign_letter(letter_match.group(1))
            else:
                print("\nИспользование: ASSIGN LETTER=X\n")
        elif command == "HELP":
            self.show_help()
        elif command == "EXIT":
            self.exit_program()
        else:
            print(f"\nНеизвестная команда: {command}")
            print("Введите HELP для списка команд\n")
    
    def run(self):
        """Запуск эмулятора"""
        print("=" * 50)
        print("Добро пожаловать в эмулятор DISKPART")
        print("=" * 50)
        self.show_help()
        
        while self.running:
            try:
                command = input("DISKPART> ")
                if command.strip():
                    self.parse_command(command)
            except KeyboardInterrupt:
                print("\n\nПрерывание...")
                self.exit_program()
            except Exception as e:
                print(f"\nОшибка: {e}\n")

if __name__ == "__main__":
    emulator = DiskpartEmulator()
    emulator.run()