from random import randint
import requests

class Pokemon:
    pokemons = {}
    
    # Инициализация объекта (конструктор)
    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer   
        self.pokemon_number = randint(1, 1000)
        
        # Делаем один общий запрос, чтобы достать все данные сразу
        self.get_pokemon_data()
        
        Pokemon.pokemons[pokemon_trainer] = self

    # Метод для получения ВСЕХ данных покемона за один раз
    def get_pokemon_data(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            # 1. Забираем имя и картинку
            self.name = data['forms'][0]['name'].capitalize() # Делаем имя с большой буквы
            self.img = data['sprites']["other"]['official-artwork']['front_default']
            
            # 2. Забираем новые свойства из API (здоровье, атаку и базовый опыт)
            self.hp = data['stats'][0]['base_stat']      # HP обычно идет первым в списке stats
            self.attack = data['stats'][1]['base_stat']  # Attack идет вторым
            self.experience = data.get('base_experience', 50) # Опыт покемона
            
        else:
            # Если сайт упал, ставим стандартные настройки (запасной вариант)
            self.name = "Pikachu"
            self.img = "error"
            self.hp = 100
            self.attack = 55
            self.experience = 60

    # Метод для вывода подробной информации о покемоне
    def info(self):
        return f"👾 Имя: {self.name}\n❤️ Здоровье (HP): {self.hp}\n⚔️ Атака: {self.attack}\n✨ Опыт: {self.experience}"

    # Метод для получения картинки покемона
    def show_img(self):
        return self.img

    # Новые методы для изменения свойств (например, если покемон подлечился или прокачался)
    def change_hp(self, count):
        """Изменяет здоровье покемона (лечение или урон)"""
        self.hp += count
        if self.hp < 0:
            self.hp = 0

    def add_experience(self, count):
        """Добавляет опыт покемону и немного увеличивает его атаку"""
        self.experience += count
        self.attack += int(count * 0.1) # За каждые 10 опыта даем +1 к атаке