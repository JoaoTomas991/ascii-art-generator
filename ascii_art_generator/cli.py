"""
Command Line Interface for ASCII Art Generator
"""

import sys
import time
import re
from typing import Callable, Dict, Any, Optional, Tuple

from .ascii_art import (
    text_to_ascii, draw_rectangle, draw_triangle, draw_circle,
    draw_heart, draw_diamond, generate_gradient, generate_checkerboard,
    generate_spiral, generate_tree, random_abstract, random_face,
    random_animal, random_emoji, create_banner, create_box,
    get_available_fonts, spinner_animation, progress_bar,
    get_color_code, get_border_chars, get_fill_style_pattern
)
from .smart_generator import (
    smart_gen, apply_fill_pattern, apply_border,
    draw_star, draw_hexagon, draw_oval, draw_arrow, draw_pentagon,
    draw_butterfly, draw_flower, get_available_fill_patterns,
    get_available_border_styles, get_available_shapes
)


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class PTCommandParser:
    """Parser for Portuguese natural language commands."""
    
    # Mapeamento de verbos de acao
    ACTION_VERBS = {
        'desenha', 'desenhar', 'faz', 'fazer', 'cria', 'criar',
        'quer', 'quero', 'mostra', 'mostrar', 'gerar', 'gera',
        'constroi', 'construir', 'escreve', 'escrever', 'exibe', 'exibir',
        'converter', 'converte', 'transforma', 'transformar', 'digita'
    }
    
    # Sinonimos para formas
    SHAPE_SYNONYMS = {
        # Formas basicas
        'retangulo': ['retângulo', 'retangulo', 'rectangulo', 'quadrado', 'caixa'],
        'triangulo': ['triângulo', 'triangulo', 'piramide', 'pirâmide'],
        'circulo': ['círculo', 'circulo', 'círculo', 'bola', 'roda'],
        'coracao': ['coração', 'coracao', 'heart'],
        'diamante': ['diamante', 'losango', 'rombo'],
        'arvore': ['árvore', 'arvore', 'natal', 'pinheiro', 'tree'],
        # Padroes
        'gradiente': ['gradiente', 'degrade', 'degradê'],
        'tabuleiro': ['tabuleiro', 'xadrez', 'checkerboard', 'tabuleiro de xadrez'],
        'espiral': ['espiral', 'caracol', 'voluta'],
        # Random
        'cara': ['cara', 'rosto', 'face', 'emoji', 'emoticon'],
        'animal': ['animal', 'bicho', 'criatura', 'corvo', 'raven', 'gato', 'cachorro', 'coelho', 'urso', 'peixe', 'pinguim', 'coruja'],
        'aleatorio': ['aleatório', 'aleatorio', 'random', 'ao acaso', 'qualquer'],
        'abstrato': ['abstrato', 'arte', 'pintura'],
        # Animais específicos
        'corvo': ['corvo', 'raven', 'graxa'],
        'gato': ['gato', 'cat'],
        'cachorro': ['cachorro', 'dog', 'cao', 'cão'],
        'coelho': ['coelho', 'rabbit', 'lebre'],
        'urso': ['urso', 'bear', 'urso pardo'],
        'peixe': ['peixe', 'fish', 'peixinho'],
        'pinguim': ['pinguim', 'penguin'],
        'coruja': ['coruja', 'owl', 'mochuelo'],
        # Texto
        'texto': ['texto', 'palavra', 'frase', 'letra', 'nome'],
        'banner': ['banner', 'faixa', 'titulo', 'cabeçalho'],
        'caixa': ['caixa', 'box', 'quadro', 'molde'],
    }
    
    # Direcoes para triangulo (mapeado para os nomes em ingles que a funcao espera)
    DIRECTION_SYNONYMS = {
        'up': ['cima', 'up', 'para cima', 'acima'],
        'down': ['baixo', 'down', 'para baixo', 'abaixo'],
        'left': ['esquerda', 'left', 'para esquerda'],
        'right': ['direita', 'right', 'para direita'],
    }
    
    # Parametros especiais
    SPECIAL_PARAMS = {
        'preenchido': ['preenchido', 'cheio', 'filled', 'sim', 'yes'],
        'vazio': ['vazio', 'oco', 'hollow', 'nao', 'não', 'no'],
    }
    
    # Palavras de combinacao para comandos compostos
    COMBINATION_WORDS = {
        'e', 'com', 'mais', 'tambem', 'também', 'tambm', 'também ', 'tmb',
        'and', 'with', 'also', 'plus'
    }
    
    # Sinonimos para fontes
    FONT_SYNONYMS = {
        'small': ['small', 'pequena', 'normal', 'padrao'],
        'block': ['block', 'bloco', 'cheia', 'solida'],
        'banner': ['banner', 'grande', 'faixa'],
        'shadow': ['shadow', 'sombra', '3d'],
    }
    
    # Sinonimos para estilos de preenchimento
    FILL_STYLE_SYNONYMS = {
        'solid': ['solido', 'cheio', 'solid', 'filled'],
        'empty': ['vazio', 'oco', 'empty', 'hollow'],
        'dotted': ['pontilhado', 'pontos', 'dotted'],
        'striped': ['listrado', 'listras', 'striped', 'riscado'],
        'striped_h': ['listrado horizontal', 'listrado h', 'striped h'],
        'striped_v': ['listrado vertical', 'listrado v', 'striped v'],
        'crosshatch': ['xadrez', 'crosshatch', 'cruzado'],
        'plus': ['mais', 'cruz', 'plus'],
        'star': ['estrela', 'asterisco', 'star'],
        'gradient': ['gradiente', 'degrade', 'degradê'],
        'random': ['aleatorio', 'aleatório', 'random'],
    }
    
    # Sinonimos para cores
    COLOR_SYNONYMS = {
        'red': ['vermelho', 'vermelha', 'red', 'encarnado', 'encarnada'],
        'green': ['verde', 'green'],
        'blue': ['azul', 'blue'],
        'yellow': ['amarelo', 'amarela', 'yellow'],
        'cyan': ['ciano', 'cyan'],
        'magenta': ['magenta', 'roxo', 'roxa'],
        'white': ['branco', 'branca', 'white'],
        'black': ['preto', 'preta', 'black'],
        'bright_red': ['vermelho claro', 'vermelha claro', 'bright red'],
        'bright_green': ['verde claro', 'bright green'],
        'bright_blue': ['azul claro', 'bright blue'],
        'bright_yellow': ['amarelo claro', 'amarela claro', 'bright yellow'],
        'reset': ['normal', 'reset', 'padrao'],
    }
    
    # Sinonimos para estilos de borda
    BORDER_STYLE_SYNONYMS = {
        'simple': ['simples', 'simple', 'normal'],
        'double': ['dupla', 'double', 'duplo'],
        'dashed': ['tracejada', 'dashed', 'tracejado'],
        'wavy': ['ondulada', 'wavy', 'ondado'],
        'bold': ['negrito', 'bold', 'grossa'],
        'light': ['fino', 'light', 'leve'],
        'star': ['estrela', 'star'],
        'plus': ['mais', 'plus', 'cruz'],
    }
    
    def __init__(self):
        # Inverter sinonimos para lookup rapido
        self.shape_to_key = {}
        for key, synonyms in self.SHAPE_SYNONYMS.items():
            for syn in synonyms:
                # Adicionar sinonimo original em lowercase
                self.shape_to_key[syn.lower()] = key
                # Adicionar tambem sem acentos para matching mais robusto
                syn_no_accents = self._remove_accents(syn).lower()
                if syn_no_accents not in self.shape_to_key:
                    self.shape_to_key[syn_no_accents] = key
        
        self.direction_to_key = {}
        for key, synonyms in self.DIRECTION_SYNONYMS.items():
            for syn in synonyms:
                self.direction_to_key[syn.lower()] = key
                syn_no_accents = self._remove_accents(syn).lower()
                if syn_no_accents not in self.direction_to_key:
                    self.direction_to_key[syn_no_accents] = key
        
        self.special_to_key = {}
        for key, synonyms in self.SPECIAL_PARAMS.items():
            for syn in synonyms:
                self.special_to_key[syn.lower()] = key
        
        # Mapeamento de fontes
        self.font_to_key = {}
        for key, synonyms in self.FONT_SYNONYMS.items():
            for syn in synonyms:
                self.font_to_key[syn.lower()] = key
                syn_no_accents = self._remove_accents(syn).lower()
                if syn_no_accents not in self.font_to_key:
                    self.font_to_key[syn_no_accents] = key
        
        # Mapeamento de estilos de preenchimento
        self.fill_style_to_key = {}
        for key, synonyms in self.FILL_STYLE_SYNONYMS.items():
            for syn in synonyms:
                self.fill_style_to_key[syn.lower()] = key
                syn_no_accents = self._remove_accents(syn).lower()
                if syn_no_accents not in self.fill_style_to_key:
                    self.fill_style_to_key[syn_no_accents] = key
        
        # Mapeamento de cores
        self.color_to_key = {}
        for key, synonyms in self.COLOR_SYNONYMS.items():
            for syn in synonyms:
                self.color_to_key[syn.lower()] = key
                syn_no_accents = self._remove_accents(syn).lower()
                if syn_no_accents not in self.color_to_key:
                    self.color_to_key[syn_no_accents] = key
        
        # Mapeamento de estilos de borda
        self.border_style_to_key = {}
        for key, synonyms in self.BORDER_STYLE_SYNONYMS.items():
            for syn in synonyms:
                self.border_style_to_key[syn.lower()] = key
                syn_no_accents = self._remove_accents(syn).lower()
                if syn_no_accents not in self.border_style_to_key:
                    self.border_style_to_key[syn_no_accents] = key
    
    def extract_numbers(self, text: str) -> list:
        """Extrai todos os numeros de um texto."""
        # Padroes: 10, 10x5, 10 x 5, 10-5, 10:5, 10,5
        patterns = [
            r'(\d+)\s*x\s*(\d+)',  # 10x5 ou 10 x 5
            r'(\d+)[-:](\d+)',       # 10-5 ou 10:5
            r'(\d+),(\d+)',         # 10,5
        ]
        numbers = []
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                numbers.extend([int(n) for n in match])
        
        # Numeros isolados
        isolated = re.findall(r'\b(\d+)\b', text)
        for num in isolated:
            if int(num) not in numbers:
                numbers.append(int(num))
        
        return numbers
    
    def extract_char(self, text: str) -> Optional[str]:
        """Extrai um caracter de desenho do texto."""
        # Padroes: "com #", "usando *", "char @", "caracter +"
        patterns = [
            r'[cC]om\s+["\']?([#*O@+=\-_\.\s])["\']?',
            r'usando\s+["\']?([#*O@+=\-_\.\s])["\']?',
            r'[cC]har\s+["\']?([#*O@+=\-_\.\s])["\']?',
            r'caracter\s+["\']?([#*O@+=\-_\.\s])["\']?',
            r'simbolo\s+["\']?([#*O@+=\-_\.\s])["\']?',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                char = match.group(1)
                if char and char != ' ':
                    return char
        return None
    
    def extract_text(self, text: str) -> Optional[str]:
        """Extrai texto para conversao em ASCII art."""
        import re as _re
        
        # Padroes: "texto HELLO", "palavra ASCII", entre aspas
        patterns = [
            r'[tT]exto\s+"([^"]+)"',
            r'[tT]exto\s+\'([^\']+)\'',
            r'[pP]alavra\s+"([^"]+)"',
            r'[pP]alavra\s+\'([^\']+)\'',
            r'[fF]rase\s+"([^"]+)"',
            r'[fF]rase\s+\'([^\']+)\'',
            r'escreve\s+"([^"]+)"',
            r'escreve\s+\'([^\']+)\'',
            r'converter\s+"([^"]+)"',
            r'converter\s+\'([^\']+)\'',
            r'banner\s+"([^"]+)"',
            r'banner\s+\'([^\']+)\'',
        ]
        
        for pattern in patterns:
            match = _re.search(pattern, text, _re.IGNORECASE)
            if match:
                return match.group(1)
        
        # Se nao encontrado em aspas, procurar por palavras maiusculas
        # que nao sao verbos ou palavras de comando
        words = text.split()
        
        # Stop words (palavras para ignorar)
        stop_words = {
            'um', 'uma', 'uns', 'umas', 'o', 'a', 'os', 'as',
            'de', 'do', 'da', 'no', 'na', 'em', 'com', 'para', 'por',
            'um', 'uma', 'o', 'a', 'os', 'as',
            'desenha', 'desenhar', 'faz', 'fazer', 'cria', 'criar',
            'quer', 'quero', 'mostra', 'mostrar', 'gerar', 'gera',
            'constroi', 'construir', 'escreve', 'escrever', 'exibe', 'exibir',
            'converter', 'converte', 'transforma', 'transformar', 'digita',
            'com', 'como', 'em', 'de', 'do', 'da', 'no', 'na',
            'ASCII', 'ascii', 'em'
        }
        
        # Verificar se ha verbos de acao
        has_action_verb = any(
            self._remove_accents(word.lower()) in self.ACTION_VERBS
            for word in words[:3]
        )
        
        if has_action_verb:
            extracted = []
            for i, word in enumerate(words):
                w_lower = word.lower()
                w_clean = self._remove_accents(w_lower)
                
                # Ignorar stop words e verbos de acao
                if w_clean in self.ACTION_VERBS or w_lower in stop_words:
                    continue
                
                # Ignorar palavras muito curtas (1 letra)
                if len(word) <= 1:
                    continue
                
                # Palavra valida para texto
                # Se for maiuscula ou title case, ou numero
                if word.isupper() or word.istitle() or (word.isdigit() and len(word) > 1):
                    extracted.append(word)
                # Se for minuscula mas parece ser texto (ex: "ola" -> "OLA")
                elif word.islower() and not word.isdigit():
                    extracted.append(word.upper())
            
            if extracted:
                return ' '.join(extracted)
        
        return None
    
    def parse_command(self, user_input: str) -> Optional[Dict[str, Any]]:
        """
        Parse natural language Portuguese command.
        Returns dict with: {'command': str, 'params': dict, 'text': str, 'compound': bool, 'parts': list}
        For compound commands, returns a list of command dicts in 'parts'
        """
        if not user_input or not user_input.strip():
            return None
        
        # Verificar se e um comando composto
        compound_parts = self._split_compound_command(user_input)
        
        if len(compound_parts) > 1:
            # Processar cada parte individualmente
            parsed_parts = []
            for part in compound_parts:
                part_result = self._parse_single_command(part, user_input)
                if part_result:
                    parsed_parts.append(part_result)
            
            if parsed_parts:
                return {
                    'command': 'compound',
                    'params': {},
                    'compound': True,
                    'parts': parsed_parts
                }
            return None
        
        # Comando simples
        return self._parse_single_command(user_input, user_input)
    
    def _parse_single_command(self, user_input: str, original_input: str = '') -> Optional[Dict[str, Any]]:
        """Parse a single (non-compound) command."""
        text = user_input.lower().strip()
        
        # Remover pontuacao
        text = re.sub(r'[?!.,;:]', '', text)
        
        # Extrair numeros
        numbers = self.extract_numbers(user_input if user_input == original_input else original_input)
        
        # Extrair caracter
        char = self.extract_char(user_input if user_input == original_input else original_input)
        
        # Extrair texto
        extracted_text = self.extract_text(user_input if user_input == original_input else original_input)
        
        # Extrair estilo, fonte, cor, borda do texto atual (para que cada parte do comando composto tenha os seus proprios parametros)
        font = self.extract_font(user_input if user_input == original_input else user_input) or 'small'
        fill_style = self.extract_fill_style(user_input if user_input == original_input else user_input)
        color = self.extract_color(user_input if user_input == original_input else user_input)
        border_style = self.extract_border_style(user_input if user_input == original_input else user_input)
        
        # Identificar acao e forma
        words = text.split()
        
        # Filtrar verbos de acao
        action_words = [w for w in words if w in self.ACTION_VERBS]
        
        # Se nao ha verbos de acao, adicionar um padrao para comandos compostos
        if not action_words and words:
            # Verificar se a primeira palavra e uma forma
            first_word = words[0]
            first_clean = self._remove_accents(first_word)
            if first_clean in self.shape_to_key:
                # Adicionar verbo padrao
                action_words = ['desenha']
                # Remover a forma da lista de palavras para nao duplicar
                words = ['desenha'] + words
        
        # Filtrar palavras de forma
        shape_words = []
        for w in words:
            if w in self.shape_to_key:
                shape_words.append(self.shape_to_key[w])
        
        # Se nao encontrado, procurar por palavras similares
        if not shape_words:
            for w in words:
                # Remover acentos para matching
                w_clean = self._remove_accents(w)
                if w_clean in self.shape_to_key:
                    shape_words.append(self.shape_to_key[w_clean])
        
        # Determinar forma principal
        shape = shape_words[0] if shape_words else None
        
        # Se nao ha verbo de acao mas ha forma, adicionar verbo padrao
        if not action_words and shape and words:
            action_words = ['desenha']
        
        # Verificar se o verbo de acao e especifico para texto
        # Se sim, e houver uma palavra que tambem e uma fonte, trata como text_to_ascii
        text_action_verbs = {'escreve', 'escrever', 'converter', 'converte', 'transforma', 'transformar', 'digita'}
        if action_words and any(verb in text_action_verbs for verb in action_words):
            # Verificar se ha palavras que sao fontes
            for w in words:
                if w in self.font_to_key:
                    # Esta e uma fonte, trata como text_to_ascii
                    if extracted_text:
                        shape = 'texto'
                    break
        
        # Casos especiais - verificar por ordem de especificidade
        
        # 1. Banner
        if shape == 'banner':
            banner_text = self._extract_banner_text(user_input, words, action_words)
            width = numbers[0] if numbers else 50
            border_char = char or '='
            return {
                'command': 'banner',
                'params': {
                    'text': banner_text or 'ASCII',
                    'width': width,
                    'char': border_char,
                    'font': font,
                    'color': color,
                    'border_style': border_style
                }
            }
        
        # 2. Caixa
        if shape == 'caixa':
            box_text = self._extract_banner_text(user_input, words, action_words)
            c = char or '#'
            return {
                'command': 'box',
                'params': {
                    'text': box_text or 'Hello\nWorld',
                    'char': c,
                    'color': color,
                    'border_style': border_style
                }
            }
        
        # 3. Formas geometricas
        if shape == 'retangulo':
            width = numbers[0] if len(numbers) >= 1 else 10
            height = numbers[1] if len(numbers) >= 2 else 5
            c = char or '#'
            
            # Verificar estilo de preenchimento
            if fill_style:
                if fill_style in ['empty', 'vazio', 'oco', 'hollow']:
                    filled = False
                    c = ' '
                elif fill_style == 'solid':
                    filled = True
                elif fill_style in ['dotted', 'pontilhado']:
                    filled = True
                    c = '.'
                elif fill_style in ['striped', 'striped_h', 'listrado']:
                    filled = True
                    c = '-'
                elif fill_style in ['striped_v']:
                    filled = True
                    c = '|'
                elif fill_style in ['crosshatch', 'xadrez']:
                    filled = True
                    c = 'X'
                elif fill_style in ['plus', 'cruz']:
                    filled = True
                    c = '+'
                elif fill_style in ['star', 'estrela']:
                    filled = True
                    c = '*'
                else:
                    filled = True
            else:
                filled = True  # default
            
            # Verificar se e preenchido ou vazio (palavras diretas)
            if not fill_style:
                for w in words:
                    if w.lower() in ['vazio', 'oco', 'hollow', 'nao', 'não']:
                        filled = False
                    elif w.lower() in ['preenchido', 'cheio', 'filled', 'sim']:
                        filled = True
            
            return {
                'command': 'rectangle',
                'params': {
                    'width': width,
                    'height': height,
                    'char': c,
                    'filled': filled,
                    'color': color,
                    'style': fill_style
                }
            }
        
        if shape == 'triangulo':
            height = numbers[0] if numbers else 5
            c = char or '*'
            direction = 'up'  # default
            
            # Procurar direcao
            for w in words:
                w_clean = self._remove_accents(w)
                if w_clean in self.direction_to_key:
                    direction = self.direction_to_key[w_clean]
            
            return {
                'command': 'triangle',
                'params': {
                    'height': height,
                    'char': c,
                    'direction': direction,
                    'color': color,
                    'style': fill_style
                }
            }
        
        if shape == 'circulo':
            radius = numbers[0] if numbers else 5
            c = char or 'O'
            return {
                'command': 'circle',
                'params': {
                    'radius': radius,
                    'char': c,
                    'color': color,
                    'style': fill_style
                }
            }
        
        if shape == 'coracao':
            size = numbers[0] if numbers else 2
            c = char or '*'
            return {
                'command': 'heart',
                'params': {
                    'size': min(max(size, 1), 3),
                    'char': c,
                    'color': color,
                    'style': fill_style
                }
            }
        
        if shape == 'diamante':
            size = numbers[0] if numbers else 5
            c = char or '*'
            return {
                'command': 'diamond',
                'params': {
                    'size': size,
                    'char': c,
                    'color': color,
                    'style': fill_style
                }
            }
        
        if shape == 'arvore':
            height = numbers[0] if numbers else 5
            c = char or '*'
            return {
                'command': 'tree',
                'params': {
                    'height': height,
                    'char': c,
                    'color': color,
                    'style': fill_style
                }
            }
        
        # 3. Padroes
        if shape == 'gradiente':
            width = numbers[0] if len(numbers) >= 1 else 10
            height = numbers[1] if len(numbers) >= 2 else 5
            return {
                'command': 'gradient',
                'params': {
                    'width': width,
                    'height': height,
                    'color': color,
                    'style': fill_style
                }
            }
        
        if shape == 'tabuleiro':
            size = numbers[0] if numbers else 8
            chars = char or '# '
            if len(chars) < 2:
                chars = '# '
            return {
                'command': 'checkerboard',
                'params': {
                    'size': size,
                    'chars': chars,
                    'color': color,
                    'style': fill_style
                }
            }
        
        if shape == 'espiral':
            size = numbers[0] if numbers else 10
            c = char or '*'
            return {
                'command': 'spiral',
                'params': {
                    'size': size,
                    'char': c,
                    'color': color,
                    'style': fill_style
                }
            }
        
        # 4. Texto para ASCII (deve ser verificado depois das formas)
        if shape == 'texto' or (extracted_text and not shape):
            text_for_ascii = extracted_text or ' '.join(words[len(action_words):])
            if text_for_ascii:
                return {
                    'command': 'text_to_ascii',
                    'params': {
                        'text': text_for_ascii,
                        'font': font,
                        'color': color,
                        'style': fill_style
                    }
                }
        
        # 5. Aleatorios
        if shape in ['cara', 'face', 'emoji']:
            return {
                'command': 'random_face',
                'params': {}
            }
        
        if shape == 'animal':
            return {
                'command': 'random_animal',
                'params': {}
            }
        
        if shape in ['aleatorio', 'abstrato']:
            width = numbers[0] if len(numbers) >= 1 else 20
            height = numbers[1] if len(numbers) >= 2 else 10
            return {
                'command': 'random_art',
                'params': {
                    'width': width,
                    'height': height
                }
            }
        
        # 5. Animacoes
        if 'animacao' in text or 'animação' in text or 'spinner' in text or 'carregando' in text or 'loading' in text:
            return {
                'command': 'spinner',
                'params': {'duration': 2.0}
            }
        
        if 'progresso' in text or 'progress' in text or 'barra' in text:
            return {
                'command': 'progress_bar',
                'params': {'duration': 3.0}
            }
        
        # 6. Showcase (so se nao houver forma especifica)
        if not shape and ('mostra' in text or 'showcase' in text or 'demonstracao' in text or 'demonstração' in text or 'exemplos' in text):
            return {
                'command': 'showcase',
                'params': {}
            }
        
        # 7. Ajuda
        if 'ajuda' in text or 'help' in text or 'socorro' in text or 'como' in text or '?' in user_input:
            return {
                'command': 'help',
                'params': {}
            }
        
        # 8. Sair
        if 'sair' in text or 'quit' in text or 'exit' in text or 'adeus' in text or 'tchau' in text:
            return {
                'command': 'quit',
                'params': {}
            }
        
        # 9. Animais específicos
        if shape == 'corvo':
            return {
                'command': 'specific_animal',
                'params': {'animal': 'crow'}
            }
        if shape == 'gato':
            return {
                'command': 'specific_animal',
                'params': {'animal': 'cat'}
            }
        if shape == 'cachorro':
            return {
                'command': 'specific_animal',
                'params': {'animal': 'dog'}
            }
        if shape == 'coelho':
            return {
                'command': 'specific_animal',
                'params': {'animal': 'rabbit'}
            }
        if shape == 'urso':
            return {
                'command': 'specific_animal',
                'params': {'animal': 'bear'}
            }
        if shape == 'peixe':
            return {
                'command': 'specific_animal',
                'params': {'animal': 'fish'}
            }
        if shape == 'pinguim':
            return {
                'command': 'specific_animal',
                'params': {'animal': 'penguin'}
            }
        if shape == 'coruja':
            return {
                'command': 'specific_animal',
                'params': {'animal': 'owl'}
            }
        
        # 10. Tentar interpretar sem forma especifica
        # Se tem numeros, pode ser uma forma padrao
        if numbers:
            if len(numbers) >= 2:
                return {
                    'command': 'rectangle',
                    'params': {
                        'width': numbers[0],
                        'height': numbers[1],
                        'char': char or '#',
                        'filled': True
                    }
                }
            else:
                return {
                    'command': 'heart',
                    'params': {
                        'size': min(max(numbers[0], 1), 3),
                        'char': char or '*'
                    }
                }
        
        return None
    
    def _split_compound_command(self, user_input: str) -> list:
        """Split a compound command into individual commands."""
        text = user_input.lower().strip()
        words = text.split()
        
        # Palavras que indicam que "com" não é uma palavra de combinação
        param_keywords = {
            'cor', 'fonte', 'estilo', 'borda', 'preenchimento',
            'char', 'caracter', 'simbolo', 'tamanho', 'largura', 'altura',
            'texto', 'palavra', 'frase', 'nome', 'letra', 'conteudo'
        }
        
        # Procurar por palavras de combinacao, ignorando "com" quando seguido de keyword
        split_positions = []
        for i, word in enumerate(words):
            if word in self.COMBINATION_WORDS:
                # Se for "com" e a próxima palavra for um keyword de parâmetro, não dividir
                if word in ['com', 'com '] and i + 1 < len(words):
                    next_word = words[i + 1]
                    if next_word in param_keywords:
                        continue
                # Se for "e" mas a próxima ou anterior palavra for um keyword de parâmetro, não dividir
                if word in ['e', 'e '] and i + 1 < len(words):
                    next_word = words[i + 1]
                    if next_word in param_keywords:
                        continue
                if word in ['e', 'e '] and i > 0:
                    prev_word = words[i - 1]
                    if prev_word in param_keywords:
                        continue
                split_positions.append(i)
        
        if not split_positions:
            return [user_input]
        
        # Dividir o comando nas posicoes das palavras de combinacao
        parts = []
        start = 0
        
        for pos in split_positions:
            # Pegar palavras do start ate antes da palavra de combinacao
            part_words = words[start:pos]
            if part_words:
                parts.append(' '.join(part_words))
            start = pos + 1
        
        # Adicionar a ultima parte
        if start < len(words):
            parts.append(' '.join(words[start:]))
        
        # Se so tiveram partes validas, retornar
        if len(parts) > 1:
            return parts
        
        return [user_input]
    
    def _extract_banner_text(self, user_input: str, words: list, action_words: list) -> Optional[str]:
        """Extract text for banner/box, removing command words."""
        # Palavras para ignorar em banner/caixa - criar uma lista completa
        ignore_words = set({
            'faz', 'fazer', 'cria', 'criar', 'desenha', 'desenhar',
            'quer', 'quero', 'mostra', 'mostrar',
            'um', 'uma', 'o', 'a', 'os', 'as',
            'banner', 'caixa', 'box', 'de', 'do', 'da', 'no', 'na', 'com', 'para',
            'texto', 'cor', 'fonte', 'estilo', 'borda', 'preenchimento'
        })
        # Adicionar todas as palavras de cor, fonte, estilo e borda
        ignore_words.update(self.color_to_key.keys())
        ignore_words.update(self.font_to_key.keys())
        ignore_words.update(self.fill_style_to_key.keys())
        ignore_words.update(self.border_style_to_key.keys())
        
        extracted = []
        # Manter o case original das palavras
        for word in words:
            w_lower = word.lower()
            if w_lower in ignore_words or word.lower() in action_words:
                continue
            if len(word) > 1:  # Ignorar palavras de 1 letra
                extracted.append(word)
        
        if extracted:
            return ' '.join(extracted)
        
        # Se nao encontrado, tentar extrair texto com aspas
        text_in_quotes = self.extract_text(user_input)
        if text_in_quotes and text_in_quotes != user_input:
            return text_in_quotes
        
        return None
    
    def extract_font(self, text: str) -> Optional[str]:
        """Extrai o nome da fonte do texto."""
        patterns = [
            r'[fF]onte\s+([^\s]+)',
            r'estilo\s+([^\s]+)',
            r'com\s+([^\s]+)\s+fonte',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                font_word = match.group(1).lower()
                if font_word in self.font_to_key:
                    return self.font_to_key[font_word]
                font_clean = self._remove_accents(font_word)
                if font_clean in self.font_to_key:
                    return self.font_to_key[font_clean]
        
        # Procurar por palavras de fonte no texto
        words = text.lower().split()
        for w in words:
            if w in self.font_to_key:
                return self.font_to_key[w]
            w_clean = self._remove_accents(w)
            if w_clean in self.font_to_key:
                return self.font_to_key[w_clean]
        
        return None
    
    def extract_fill_style(self, text: str) -> Optional[str]:
        """Extrai o estilo de preenchimento do texto."""
        patterns = [
            r'[eE]stilo\s+([^\s]+)',
            r'preenchimento\s+([^\s]+)',
            r'com\s+preenchimento\s+([^\s]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                style_word = match.group(1).lower()
                if style_word in self.fill_style_to_key:
                    return self.fill_style_to_key[style_word]
                style_clean = self._remove_accents(style_word)
                if style_clean in self.fill_style_to_key:
                    return self.fill_style_to_key[style_clean]
        
        # Procurar por palavras de estilo no texto
        words = text.lower().split()
        for w in words:
            if w in self.fill_style_to_key:
                return self.fill_style_to_key[w]
            w_clean = self._remove_accents(w)
            if w_clean in self.fill_style_to_key:
                return self.fill_style_to_key[w_clean]
        
        return None
    
    def extract_color(self, text: str) -> Optional[str]:
        """Extrai a cor do texto."""
        patterns = [
            r'[cC]or\s+([^\s]+)',
            r'na\s+cor\s+([^\s]+)',
            r'com\s+a\s+cor\s+([^\s]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                color_word = match.group(1).lower()
                if color_word in self.color_to_key:
                    return self.color_to_key[color_word]
                color_clean = self._remove_accents(color_word)
                if color_clean in self.color_to_key:
                    return self.color_to_key[color_clean]
        
        # Procurar por palavras de cor no texto
        words = text.lower().split()
        for w in words:
            if w in self.color_to_key:
                return self.color_to_key[w]
            w_clean = self._remove_accents(w)
            if w_clean in self.color_to_key:
                return self.color_to_key[w_clean]
        
        return None
    
    def extract_border_style(self, text: str) -> Optional[str]:
        """Extrai o estilo de borda do texto."""
        patterns = [
            r'borda\s+([^\s]+)',
            r'estilo\s+de\s+borda\s+([^\s]+)',
            r'com\s+borda\s+([^\s]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                border_word = match.group(1).lower()
                if border_word in self.border_style_to_key:
                    return self.border_style_to_key[border_word]
                border_clean = self._remove_accents(border_word)
                if border_clean in self.border_style_to_key:
                    return self.border_style_to_key[border_clean]
        
        # Procurar por palavras de borda no texto
        words = text.lower().split()
        for w in words:
            if w in self.border_style_to_key:
                return self.border_style_to_key[w]
            w_clean = self._remove_accents(w)
            if w_clean in self.border_style_to_key:
                return self.border_style_to_key[w_clean]
        
        return None
    
    @staticmethod
    def _remove_accents(text: str) -> str:
        """Remove accents from text for better matching."""
        accent_map = {
            'á': 'a', 'à': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a',
            'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
            'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
            'ó': 'o', 'ò': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o',
            'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u',
            'ç': 'c',
            'Á': 'A', 'À': 'A', 'Â': 'A', 'Ã': 'A', 'Ä': 'A',
            'É': 'E', 'È': 'E', 'Ê': 'E', 'Ë': 'E',
            'Í': 'I', 'Ì': 'I', 'Î': 'I', 'Ï': 'I',
            'Ó': 'O', 'Ò': 'O', 'Ô': 'O', 'Õ': 'O', 'Ö': 'O',
            'Ú': 'U', 'Ù': 'U', 'Û': 'U', 'Ü': 'U',
            'Ç': 'C',
        }
        result = []
        for char in text:
            result.append(accent_map.get(char, char))
        return ''.join(result)


class Menu:
    """Interactive menu system."""
    
    def __init__(self, title: str = "ASCII Art Generator"):
        self.title = title
        self.items: Dict[str, Dict[str, Any]] = {}
        self.exit_option = ('q', 'Quit')
    
    def add_item(self, key: str, label: str, action: Callable,
                 description: str = "", category: str = "Main") -> None:
        self.items[key] = {
            'key': key, 'label': label, 'action': action,
            'description': description, 'category': category
        }
    
    def display(self) -> None:
        """Display the menu."""
        print(f"\n{Colors.HEADER}{'=' * 60}{Colors.ENDC}")
        print(f"{Colors.HEADER}{self.title:^60}{Colors.ENDC}")
        print(f"{Colors.HEADER}{'=' * 60}{Colors.ENDC}")
        
        categories = {}
        for key, item in sorted(self.items.items()):
            category = item['category']
            if category not in categories:
                categories[category] = []
            categories[category].append((key, item))
        
        for category, items in categories.items():
            if category != "Main":
                print(f"\n{Colors.OKBLUE}{category}{Colors.ENDC}")
                print("-" * len(category))
            
            for key, item in items:
                label = item['label']
                desc = item['description']
                if desc:
                    print(f"  {Colors.OKGREEN}[{key}]{Colors.ENDC} {label:20} - {desc}")
                else:
                    print(f"  {Colors.OKGREEN}[{key}]{Colors.ENDC} {label}")
        
        print(f"\n{Colors.WARNING}[{self.exit_option[0]}]{Colors.ENDC} {self.exit_option[1]}")
        print()
    
    def run(self) -> None:
        """Run the menu loop."""
        while True:
            self.display()
            choice = input(f"{Colors.BOLD}Enter your choice: {Colors.ENDC}").strip()
            
            if choice.lower() == self.exit_option[0].lower():
                print(f"\n{Colors.OKGREEN}Goodbye!{Colors.ENDC}")
                break
            
            if choice in self.items:
                try:
                    self.items[choice]['action']()
                    input(f"\n{Colors.WARNING}Press Enter to continue...{Colors.ENDC}")
                except Exception as e:
                    print(f"{Colors.FAIL}Error: {e}{Colors.ENDC}")
                    time.sleep(2)
            else:
                print(f"{Colors.FAIL}Invalid choice.{Colors.ENDC}")
                time.sleep(1)


class ENCommandParser:
    """Parser for English natural language commands."""
    
    # Action verbs
    ACTION_VERBS = {
        'draw', 'drawing', 'drew',
        'make', 'makes', 'made', 'create', 'creates', 'created', 'build', 'builds', 'built',
        'write', 'writes', 'wrote', 'type', 'types', 'typed', 'print', 'prints', 'printed',
        'show', 'shows', 'showed', 'display', 'displays', 'displayed',
        'generate', 'generates', 'generated', 'produce', 'produces', 'produced',
        'convert', 'converts', 'converted', 'transform', 'transforms', 'transformed'
    }
    
    # Synonyms for shapes
    SHAPE_SYNONYMS = {
        # Basic shapes
        'rectangle': ['rectangle', 'rect', 'square', 'box'],
        'triangle': ['triangle', 'tri', 'pyramid'],
        'circle': ['circle', 'circ', 'ball', 'wheel'],
        'heart': ['heart'],
        'diamond': ['diamond', 'rhombus'],
        'tree': ['tree', 'christmas', 'pine'],
        'star': ['star'],
        'hexagon': ['hexagon', 'hex'],
        'oval': ['oval', 'ellipse'],
        'arrow': ['arrow'],
        'pentagon': ['pentagon'],
        'butterfly': ['butterfly'],
        'flower': ['flower'],
        # Patterns
        'gradient': ['gradient', 'degrade'],
        'checkerboard': ['checkerboard', 'chessboard'],
        'random': ['random'],
        'abstract': ['abstract', 'art', 'painting'],
        # Random
        'face': ['face', 'emoji', 'emoticon'],
        'animal': ['animal', 'creature', 'crow', 'raven', 'cat', 'dog', 'rabbit', 'bear', 'fish', 'penguin', 'owl'],
        # Text
        'text': ['text', 'word', 'phrase', 'letter', 'name'],
        'banner': ['banner'],
        'box': ['box'],
        # Smart commands
        'smart': ['smart', 'surprise', 'surprise me', 'random art', 'interesting', 'amazing'],
        'minimal': ['minimal', 'simple', 'clean'],
        'complex': ['complex', 'detailed', 'elaborate'],
        'geometric': ['geometric', 'geometry'],
        'nature': ['nature'],
        'abstract': ['abstract', 'pattern', 'design'],
    }
    
    # Direction synonyms for triangle
    DIRECTION_SYNONYMS = {
        'up': ['up', 'upward'],
        'down': ['down', 'downward'],
        'left': ['left'],
        'right': ['right'],
    }
    
    # Special parameters
    SPECIAL_PARAMS = {
        'filled': ['filled', 'full', 'solid', 'yes'],
        'empty': ['empty', 'hollow', 'no'],
    }
    
    # Combination words for compound commands
    COMBINATION_WORDS = {
        'and', 'with', 'also', 'plus', 'then',
        'comma'
    }
    
    # Font synonyms
    FONT_SYNONYMS = {
        'small': ['small', 'tiny'],
        'block': ['block'],
        'banner': ['banner'],
        'shadow': ['shadow']
    }
    
    # Color synonyms
    COLOR_SYNONYMS = {
        'red': ['red', 'crimson', 'ruby'],
        'green': ['green', 'emerald'],
        'blue': ['blue', 'azure', 'cobalt'],
        'yellow': ['yellow', 'gold', 'amber'],
        'cyan': ['cyan', 'turquoise'],
        'magenta': ['magenta', 'purple', 'violet'],
        'white': ['white'],
        'black': ['black'],
        'light_red': ['light_red', 'lightred', 'pink'],
        'light_green': ['light_green', 'lightgreen'],
        'light_blue': ['light_blue', 'lightblue'],
        'light_yellow': ['light_yellow', 'lightyellow'],
        'light_cyan': ['light_cyan', 'lightcyan'],
        'light_magenta': ['light_magenta', 'lightmagenta'],
    }
    
    # Fill pattern synonyms
    FILL_PATTERN_SYNONYMS = {
        'solid': ['solid', 'filled', 'full'],
        'empty': ['empty', 'hollow'],
        'dotted': ['dotted', 'dots'],
        'striped': ['striped', 'stripes'],
        'horizontal_stripes': ['horizontal_stripes', 'horizontal', 'h_stripes'],
        'vertical_stripes': ['vertical_stripes', 'vertical', 'v_stripes'],
        'crosshatch': ['crosshatch', 'hatched'],
        'cross': ['cross'],
        'diagonal': ['diagonal'],
        'anti_diagonal': ['anti_diagonal', 'anti-diagonal'],
        'x_pattern': ['x_pattern', 'x-pattern', 'x'],
        'grid': ['grid'],
        'checkerboard': ['checkerboard', 'chessboard'],
        'dense_checkerboard': ['dense_checkerboard', 'dense-checkerboard'],
        'random': ['random'],
        'sparse_random': ['sparse_random', 'sparse-random'],
        'dense_random': ['dense_random', 'dense-random'],
        'dots': ['dots'],
        'stars': ['stars'],
        'plus_signs': ['plus_signs', 'plus-signs', 'pluses'],
        'mixed': ['mixed'],
        'left_gradient': ['left_gradient', 'left-gradient'],
        'right_gradient': ['right_gradient', 'right-gradient'],
        'top_gradient': ['top_gradient', 'top-gradient'],
        'bottom_gradient': ['bottom_gradient', 'bottom-gradient'],
        'center_gradient': ['center_gradient', 'center-gradient'],
        'spiral_pattern': ['spiral_pattern', 'spiral-pattern'],
        'concentric': ['concentric'],
        'wave': ['wave'],
        'zigzag': ['zigzag'],
        'honeycomb': ['honeycomb'],
        'plus': ['plus', 'cross'],
        'gradient': ['gradient'],
    }
    
    # Border style synonyms
    BORDER_STYLE_SYNONYMS = {
        'simple': ['simple', 'normal'],
        'double': ['double'],
        'dashed': ['dashed'],
        'dotted': ['dotted'],
        'wavy': ['wavy'],
        'bold': ['bold', 'thick'],
        'light': ['light', 'thin'],
        'thick': ['thick'],
        'fancy': ['fancy', 'decorative'],
        'rounded': ['rounded', 'curved'],
        '3d': ['3d', 'three-d', 'threed'],
        'shadow': ['shadow'],
        'double_line': ['double_line', 'double-line', 'box'],
        'star': ['star'],
        'plus': ['plus', 'cross'],
    }
    
    def __init__(self):
        """Initialize the parser."""
        self.action_to_key = {}
        for action in self.ACTION_VERBS:
            self.action_to_key[action.lower()] = 'action'
        
        # Create reverse mappings for quick lookup
        self.shape_to_key = {}
        for key, synonyms in self.SHAPE_SYNONYMS.items():
            for syn in synonyms:
                self.shape_to_key[syn.lower()] = key
        
        self.direction_to_key = {}
        for key, synonyms in self.DIRECTION_SYNONYMS.items():
            for syn in synonyms:
                self.direction_to_key[syn.lower()] = key
        
        self.font_to_key = {}
        for key, synonyms in self.FONT_SYNONYMS.items():
            for syn in synonyms:
                self.font_to_key[syn.lower()] = key
        
        self.color_to_key = {}
        for key, synonyms in self.COLOR_SYNONYMS.items():
            for syn in synonyms:
                self.color_to_key[syn.lower()] = key
        
        self.fill_to_key = {}
        for key, synonyms in self.FILL_PATTERN_SYNONYMS.items():
            for syn in synonyms:
                self.fill_to_key[syn.lower()] = key
        
        self.border_to_key = {}
        for key, synonyms in self.BORDER_STYLE_SYNONYMS.items():
            for syn in synonyms:
                self.border_to_key[syn.lower()] = key
    
    def _remove_accents(self, text: str) -> str:
        """Remove accents from text (not typically needed for English)."""
        return text
    
    def parse_command(self, command: str) -> Optional[Dict[str, Any]]:
        """Parse a natural language command and return structured data."""
        if not command or not command.strip():
            return None
        
        command_lower = command.lower().strip()
        
        # Check for intelligent mode exit commands
        if command_lower in ['menu', 'm', 'exit', 'quit', 'q', 'back']:
            return {'command': command_lower, 'action': command_lower}
        
        # Extract numbers first
        numbers = self.extract_numbers(command_lower)
        
        # Tokenize command
        tokens = command_lower.split()
        
        # Find action verb
        action = None
        action_idx = -1
        for i, token in enumerate(tokens):
            if token in self.ACTION_VERBS:
                action = token
                action_idx = i
                break
        
        if action is None:
            # Try to infer action from first token
            if tokens:
                action = tokens[0]
                action_idx = 0
        
        # Find shape/object
        shape = None
        shape_idx = -1
        
        if action_idx >= 0:
            # Look for shape in remaining tokens
            for i in range(action_idx + 1, len(tokens)):
                token = tokens[i]
                if token in self.shape_to_key:
                    shape = self.shape_to_key[token]
                    shape_idx = i
                    break
                
                # Check for "a/an/the" prefix
                if i > 0 and tokens[i-1] in ['a', 'an', 'the']:
                    if token in self.shape_to_key:
                        shape = self.shape_to_key[token]
                        shape_idx = i
                        break
        
        # If no shape found, check if it's a text command
        if shape is None and action in ['write', 'type', 'print', 'convert']:
            shape = 'text'
            # Find the text content
            text_start = action_idx + 1
            if text_start < len(tokens):
                # Skip "a/an/the" if present
                if tokens[text_start] in ['a', 'an', 'the']:
                    text_start += 1
                shape_idx = text_start
        
        # If still no shape, try to find it differently
        if shape is None:
            for i, token in enumerate(tokens):
                if token in self.shape_to_key:
                    shape = self.shape_to_key[token]
                    shape_idx = i
                    break
        
        # Extract parameters
        params = {}
        
        if shape_idx >= 0 and shape_idx + 1 < len(tokens):
            # Get remaining tokens after shape
            remaining = tokens[shape_idx + 1:]
            
            i = 0
            while i < len(remaining):
                token = remaining[i]
                
                # Check for "with", "of", "in", "using" etc.
                if token in ['with', 'of', 'in', 'using', 'for', 'as']:
                    i += 1
                    continue
                
                # Check for parameters with values
                if i + 1 < len(remaining):
                    next_token = remaining[i + 1]
                    
                    # Check for size/dimension parameters
                    if token in ['size', 'width', 'height', 'radius', 'base', 'diameter']:
                        if next_token.isdigit():
                            params[token] = int(next_token)
                            i += 2
                            continue
                        else:
                            i += 1
                            continue
                    
                    # Check for color
                    elif token in ['color', 'colour']:
                        if next_token in self.color_to_key:
                            params['color'] = self.color_to_key[next_token]
                        else:
                            params['color'] = next_token
                        i += 2
                        continue
                    
                    # Check for font
                    elif token in ['font', 'style']:
                        if next_token in self.font_to_key:
                            params['font'] = self.font_to_key[next_token]
                        else:
                            params['font'] = next_token
                        i += 2
                        continue
                    
                    # Check for fill
                    elif token in ['fill', 'filled', 'pattern']:
                        if next_token in self.fill_to_key:
                            params['fill'] = self.fill_to_key[next_token]
                        else:
                            params['fill'] = next_token
                        i += 2
                        continue
                    
                    # Check for border
                    elif token in ['border', 'edge']:
                        if next_token in self.border_to_key:
                            params['border'] = self.border_to_key[next_token]
                        else:
                            params['border'] = next_token
                        i += 2
                        continue
                    
                    # Check for direction
                    elif token in ['direction', 'dir']:
                        if next_token in self.direction_to_key:
                            params['direction'] = self.direction_to_key[next_token]
                        else:
                            params['direction'] = next_token
                        i += 2
                        continue
                
                # Check for standalone parameters
                if token in ['solid', 'filled', 'empty', 'hollow']:
                    params['fill'] = token
                    i += 1
                    continue
                
                if token in self.color_to_key:
                    params['color'] = self.color_to_key[token]
                    i += 1
                    continue
                
                if token in self.font_to_key:
                    params['font'] = self.font_to_key[token]
                    i += 1
                    continue
                
                if token in self.fill_to_key:
                    params['fill'] = self.fill_to_key[token]
                    i += 1
                    continue
                
                if token in self.border_to_key:
                    params['border'] = self.border_to_key[token]
                    i += 1
                    continue
                
                # Extract text content for text commands
                if shape == 'text' and 'text' not in params:
                    params['text'] = token
                    i += 1
                    # Collect remaining tokens as text
                    while i < len(remaining):
                        params['text'] += ' ' + remaining[i]
                        i += 1
                    continue
                
                i += 1
        
        # Map shape to command name
        shape_to_command = {
            'rectangle': 'rectangle',
            'square': 'rectangle',
            'box': 'rectangle',
            'triangle': 'triangle',
            'pyramid': 'triangle',
            'circle': 'circle',
            'ball': 'circle',
            'wheel': 'circle',
            'heart': 'heart',
            'diamond': 'diamond',
            'rhombus': 'diamond',
            'spiral': 'spiral',
            'snail': 'spiral',
            'volute': 'spiral',
            'tree': 'tree',
            'christmas_tree': 'tree',
            'star': 'star',
            'hexagon': 'hexagon',
            'hex': 'hexagon',
            'oval': 'oval',
            'ellipse': 'oval',
            'arrow': 'arrow',
            'pentagon': 'pentagon',
            'butterfly': 'butterfly',
            'flower': 'flower',
            'gradient': 'gradient',
            'degrade': 'gradient',
            'checkerboard': 'checkerboard',
            'chessboard': 'checkerboard',
            'random': 'random_art',
            'abstract': 'random_art',
            'art': 'random_art',
            'painting': 'random_art',
            'face': 'random_face',
            'emoji': 'random_emoji',
            'emoticon': 'random_emoji',
            'animal': 'random_animal',
            'creature': 'random_animal',
            'crow': 'specific_animal',
            'raven': 'specific_animal',
            'cat': 'specific_animal',
            'dog': 'specific_animal',
            'rabbit': 'specific_animal',
            'bear': 'specific_animal',
            'fish': 'specific_animal',
            'penguin': 'specific_animal',
            'owl': 'specific_animal',
            'text': 'text_to_ascii',
            'banner': 'banner',
            'box': 'box',
            # Smart commands
            'smart': 'smart',
            'surprise': 'surprise',
            'surprise me': 'surprise',
            'random art': 'random',
            'interesting': 'interesting',
            'amazing': 'amazing',
            'minimal': 'minimal',
            'simple': 'minimal',
            'clean': 'minimal',
            'complex': 'complex',
            'detailed': 'complex',
            'elaborate': 'complex',
            'geometric': 'geometric',
            'geometry': 'geometric',
            'nature': 'nature',
            'abstract': 'abstract',
            'pattern': 'abstract',
            'design': 'abstract',
        }
        
        command_name = shape_to_command.get(shape, shape) if shape else None
        
        # Build params with numbers
        final_params = params.copy()
        if numbers:
            if command_name in ['rectangle']:
                if len(numbers) >= 2:
                    final_params['width'] = numbers[0]
                    final_params['height'] = numbers[1]
                elif len(numbers) == 1:
                    final_params['width'] = numbers[0]
                    final_params['height'] = numbers[0]
            elif command_name in ['circle', 'spiral']:
                if numbers:
                    final_params['radius'] = numbers[0]
            elif command_name in ['triangle', 'diamond', 'tree']:
                if numbers:
                    final_params['size'] = numbers[0]
            elif command_name == 'heart':
                if numbers:
                    final_params['size'] = min(max(numbers[0], 1), 3)
            elif command_name in ['checkerboard', 'gradient', 'random_art']:
                if numbers:
                    final_params['size'] = numbers[0]
        
        # Add char if not specified
        if 'char' not in final_params:
            final_params['char'] = '#'
        
        # Handle text commands
        if command_name == 'text_to_ascii':
            if 'text' not in final_params:
                # Extract text from command
                text_start = action_idx + 1
                if text_start < len(tokens):
                    if tokens[text_start] in ['a', 'an', 'the']:
                        text_start += 1
                    text_end = shape_idx if shape_idx > text_start else len(tokens)
                    final_params['text'] = ' '.join(tokens[text_start:text_end])
        
        # Build result in the same format as PTCommandParser
        result = {
            'raw': command,
            'command': command_name,
            'params': final_params,
        }
        
        return result if command_name else None
    
    def extract_numbers(self, text: str) -> list:
        """Extract all numbers from text."""
        import re
        # Patterns: 10, 10x5, 10 x 5, 10-5, 10:5, 10,5
        patterns = [
            r'(\d+)\s*x\s*(\d+)',  # 10x5 or 10 x 5
            r'(\d+)[-:](\d+)',       # 10-5 or 10:5
            r'(\d+),(\d+)',         # 10,5
        ]
        numbers = []
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                numbers.extend([int(n) for n in match])
        
        # Isolated numbers
        isolated = re.findall(r'\b(\d+)\b', text)
        for num in isolated:
            if int(num) not in numbers:
                numbers.append(int(num))
        
        return numbers
    
    def extract_char(self, text: str) -> Optional[str]:
        """Extract a drawing character from text."""
        import re
        # Patterns: "with #", "using *", "char @"
        patterns = [
            r'[wW]ith\s+["\']?([#*O@+=\-_\.\s])["\']?',
            r'[uU]sing\s+["\']?([#*O@+=\-_\.\s])["\']?',
            r'[cC]har\s+["\']?([#*O@+=\-_\.\s])["\']?',
            r'character\s+["\']?([#*O@+=\-_\.\s])["\']?',
            r'symbol\s+["\']?([#*O@+=\-_\.\s])["\']?',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                char = match.group(1)
                if char and char != ' ':
                    return char
        return None


class ASCIIArtCLI:
    """Main CLI class for ASCII Art Generator."""
    
    def __init__(self):
        self.menu = Menu("ASCII Art Generator")
        self.setup_menu()
        self.parser = ENCommandParser()
        self.intelligent_mode = False
    
    def setup_menu(self) -> None:
        """Setup all menu items."""
        self.menu.add_item('t', 'Text to ASCII', self.menu_text_to_ascii,
                          'Convert text to ASCII art', 'Text & Fonts')
        self.menu.add_item('r', 'Rectangle', self.menu_rectangle,
                          'Draw a rectangle', 'Shapes')
        self.menu.add_item('tr', 'Triangle', self.menu_triangle,
                           'Draw a triangle', 'Shapes')
        self.menu.add_item('c', 'Circle', self.menu_circle,
                           'Draw a circle', 'Shapes')
        self.menu.add_item('h', 'Heart', self.menu_heart,
                           'Draw a heart', 'Shapes')
        self.menu.add_item('d', 'Diamond', self.menu_diamond,
                           'Draw a diamond', 'Shapes')
        self.menu.add_item('tree', 'Tree', self.menu_tree,
                           'Draw a Christmas tree', 'Shapes')
        self.menu.add_item('g', 'Gradient', self.menu_gradient,
                           'Generate a gradient', 'Patterns')
        self.menu.add_item('cb', 'Checkerboard', self.menu_checkerboard,
                           'Generate a checkerboard', 'Patterns')
        self.menu.add_item('s', 'Spiral', self.menu_spiral,
                           'Generate a spiral', 'Patterns')
        self.menu.add_item('ra', 'Random Art', self.menu_random_art,
                           'Generate random art', 'Random')
        self.menu.add_item('f', 'Random Face', self.menu_random_face,
                           'Generate a random face', 'Random')
        self.menu.add_item('a', 'Random Animal', self.menu_random_animal,
                           'Generate a random animal', 'Random')
        self.menu.add_item('e', 'Random Emoji', self.menu_random_emoji,
                           'Generate a random emoji', 'Random')
        self.menu.add_item('b', 'Banner', self.menu_banner,
                           'Create a banner', 'Text & Fonts')
        self.menu.add_item('box', 'Text Box', self.menu_box,
                           'Create a text box', 'Text & Fonts')
        self.menu.add_item('spin', 'Spinner', lambda: spinner_animation(2.0),
                           'Show a spinner', 'Animations')
        self.menu.add_item('pb', 'Progress Bar', lambda: progress_bar(3.0),
                           'Show progress bar', 'Animations')
        self.menu.add_item('show', 'Showcase', self.menu_showcase,
                           'Display showcase', 'Main')
        self.menu.add_item('i', 'Intelligent Mode', self._activate_intelligent_mode,
                           'Speak in natural English!', 'Main')
        self.menu.add_item('?', 'Help', self.menu_help,
                           'Show help', 'Main')
    
    def menu_text_to_ascii(self) -> None:
        """Text to ASCII menu."""
        print(f"\n{Colors.OKBLUE}=== Text to ASCII ==={Colors.ENDC}")
        print(f"Available fonts: {', '.join(get_available_fonts())}")
        text = input("Enter text: ").strip() or "ASCII"
        font = input("Font (small) [small]: ").strip() or 'small'
        print(f"\n{Colors.OKGREEN}{text_to_ascii(text, font)}{Colors.ENDC}")
    
    def menu_rectangle(self) -> None:
        """Rectangle menu."""
        print(f"\n{Colors.OKBLUE}=== Rectangle ==={Colors.ENDC}")
        try:
            width = int(input("Width: ") or "10")
            height = int(input("Height: ") or "5")
            char = input("Character [#]: ") or "#"
            filled = input("Filled? (y/n) [y]: ").lower() or "y"
            print(f"\n{Colors.OKGREEN}{draw_rectangle(width, height, char, filled == 'y')}{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.FAIL}Invalid input.{Colors.ENDC}")
    
    def menu_triangle(self) -> None:
        """Triangle menu."""
        print(f"\n{Colors.OKBLUE}=== Triangle ==={Colors.ENDC}")
        print("Directions: up, down, left, right")
        try:
            height = int(input("Height: ") or "5")
            char = input("Character [*]: ") or "*"
            direction = input("Direction [up]: ").strip() or "up"
            print(f"\n{Colors.OKGREEN}{draw_triangle(height, char, direction)}{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.FAIL}Invalid input.{Colors.ENDC}")
    
    def menu_circle(self) -> None:
        """Circle menu."""
        print(f"\n{Colors.OKBLUE}=== Circle ==={Colors.ENDC}")
        try:
            radius = int(input("Radius: ") or "5")
            char = input("Character [O]: ") or "O"
            print(f"\n{Colors.OKGREEN}{draw_circle(radius, char)}{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.FAIL}Invalid input.{Colors.ENDC}")
    
    def menu_heart(self) -> None:
        """Heart menu."""
        print(f"\n{Colors.OKBLUE}=== Heart ==={Colors.ENDC}")
        try:
            size = int(input("Size (1-3) [2]: ") or "2")
            char = input("Character [*]: ") or "*"
            print(f"\n{Colors.OKGREEN}{draw_heart(size, char)}{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.FAIL}Invalid input.{Colors.ENDC}")
    
    def menu_diamond(self) -> None:
        """Diamond menu."""
        print(f"\n{Colors.OKBLUE}=== Diamond ==={Colors.ENDC}")
        try:
            size = int(input("Size: ") or "5")
            char = input("Character [*]: ") or "*"
            print(f"\n{Colors.OKGREEN}{draw_diamond(size, char)}{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.FAIL}Invalid input.{Colors.ENDC}")
    
    def menu_tree(self) -> None:
        """Tree menu."""
        print(f"\n{Colors.OKBLUE}=== Christmas Tree ==={Colors.ENDC}")
        try:
            height = int(input("Height: ") or "5")
            char = input("Character [*]: ") or "*"
            print(f"\n{Colors.OKGREEN}{generate_tree(height, char)}{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.FAIL}Invalid input.{Colors.ENDC}")
    
    def menu_gradient(self) -> None:
        """Gradient menu."""
        print(f"\n{Colors.OKBLUE}=== Gradient ==={Colors.ENDC}")
        try:
            width = int(input("Width: ") or "10")
            height = int(input("Height: ") or "5")
            print(f"\n{Colors.OKGREEN}{generate_gradient(width, height)}{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.FAIL}Invalid input.{Colors.ENDC}")
    
    def menu_checkerboard(self) -> None:
        """Checkerboard menu."""
        print(f"\n{Colors.OKBLUE}=== Checkerboard ==={Colors.ENDC}")
        try:
            size = int(input("Size: ") or "8")
            chars = input("Characters [# ]: ") or "# "
            print(f"\n{Colors.OKGREEN}{generate_checkerboard(size, chars)}{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.FAIL}Invalid input.{Colors.ENDC}")
    
    def menu_spiral(self) -> None:
        """Spiral menu."""
        print(f"\n{Colors.OKBLUE}=== Spiral ==={Colors.ENDC}")
        try:
            size = int(input("Size [10]: ") or "10")
            char = input("Character [*]: ") or "*"
            print(f"\n{Colors.OKGREEN}{generate_spiral(size, char)}{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.FAIL}Invalid input.{Colors.ENDC}")
    
    def menu_random_art(self) -> None:
        """Random art menu."""
        print(f"\n{Colors.OKBLUE}=== Random Art ==={Colors.ENDC}")
        try:
            width = int(input("Width: ") or "20")
            height = int(input("Height: ") or "10")
            print(f"\n{Colors.OKGREEN}{random_abstract(width, height)}{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.FAIL}Invalid input.{Colors.ENDC}")
    
    def menu_random_face(self) -> None:
        """Random face menu."""
        print(f"\n{Colors.OKBLUE}=== Random Face ==={Colors.ENDC}")
        print(f"\n{Colors.OKGREEN}{random_face()}{Colors.ENDC}")
    
    def menu_random_animal(self) -> None:
        """Random animal menu."""
        print(f"\n{Colors.OKBLUE}=== Random Animal ==={Colors.ENDC}")
        print(f"\n{Colors.OKGREEN}{random_animal()}{Colors.ENDC}")
    
    def menu_random_emoji(self) -> None:
        """Random emoji menu."""
        print(f"\n{Colors.OKBLUE}=== Random Emoji ==={Colors.ENDC}")
        print(f"\n{Colors.OKGREEN}{random_emoji()}{Colors.ENDC}")
    
    def menu_banner(self) -> None:
        """Banner menu."""
        print(f"\n{Colors.OKBLUE}=== Banner ==={Colors.ENDC}")
        text = input("Text: ").strip() or "HELLO"
        try:
            width = int(input("Width [50]: ") or "50")
            char = input("Border char [=]: ") or "="
            print(f"\n{Colors.OKGREEN}{create_banner(text, width, char)}{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.FAIL}Invalid input.{Colors.ENDC}")
    
    def menu_box(self) -> None:
        """Box menu."""
        print(f"\n{Colors.OKBLUE}=== Text Box ==={Colors.ENDC}")
        text = input("Text: ").strip() or "Hello\nWorld"
        char = input("Border char [#]: ") or "#"
        print(f"\n{Colors.OKGREEN}{create_box(text, None, char)}{Colors.ENDC}")
    
    def _activate_intelligent_mode(self) -> None:
        """Activate intelligent mode."""
        self.intelligent_mode = True
        print(f"{Colors.OKGREEN}Activating intelligent mode...{Colors.ENDC}")
        time.sleep(0.5)
        self.run_intelligent_mode()
    
    def _get_specific_animal_art(self, animal_name: str) -> str:
        """Get ASCII art for a specific animal by name."""
        animals_art = {
            'crow': "  _~_ \n /\\  /\\ \n(  .  .  )\n  >=v=< \n /\\  /\\ \n_~_   _~_",
            'raven': "   .-^~ \n  /   @  @ \\ \n |         |\n  \\  >^<  /\n   '-...-' ",
            'cat': " /\\_/\\ \n( o.o ) \n > ^ < ",
            'dog': " /\\__/\\ \n( =.= ) \n (\" ) (\" )",
            'owl': "  /\\ \n (oo) \n /\\/\\ ",
            'penguin': "  _(__) \n <(.)__ \n  (___)",
            'fish': "  >=====| \n (     ) \n  >=====| ",
            'bear': "  (\\___/) \n  (U^._.^U) \n  /  \\  3 ",
            'rabbit': "  (\\_)~ \n  (='.'=) \n  (\" _) (\" _)",
        }
        
        return animals_art.get(animal_name, f"Animal '{animal_name}' não encontrado.")
    
    def _show_specific_animal(self, animal_name: str) -> None:
        """Show a specific animal by name."""
        art = self._get_specific_animal_art(animal_name)
        print(f"\n{Colors.OKGREEN}{art}{Colors.ENDC}")
    
    def menu_showcase(self) -> None:
        """Display showcase."""
        print(f"\n{Colors.HEADER}=== ASCII Art Showcase ==={Colors.ENDC}\n")
        print(f"{Colors.OKBLUE}Text to ASCII:{Colors.ENDC}")
        print(text_to_ascii("HELLO"))
        print()
        print(f"{Colors.OKBLUE}Shapes:{Colors.ENDC}")
        print(draw_heart(2, '*'))
        print(draw_diamond(3, '*'))
        print()
        print(f"{Colors.OKBLUE}Tree:{Colors.ENDC}")
        print(generate_tree(4))
        print()
        print(f"{Colors.OKBLUE}Random:{Colors.ENDC}")
        print(f"Face: {random_face()}")
        print(f"Animal: {random_animal()}")
        print(f"Emoji: {random_emoji()}")
        print()
        print(f"{Colors.OKBLUE}Banner:{Colors.ENDC}")
        print(create_banner("ASCII ART", 40))
        print()
    
    def menu_help(self) -> None:
        """Display help."""
        print(f"\n{Colors.HEADER}=== Help ==={Colors.ENDC}")
        print("""
ASCII Art Generator - Generate ASCII art from text, shapes and patterns

Features:
- Convert text to ASCII art with different fonts
- Draw geometric shapes (rectangle, triangle, circle, heart, diamond, star, hexagon, oval, arrow, pentagon, butterfly, flower)
- Generate patterns (gradient, checkerboard, spiral, crosshatch, honeycomb, wave, zigzag)
- Create random art, faces, animals and emojis
- Generate banners and text boxes
- Display animations (spinner, progress bar)

Usage:
- Type a menu option to select it
- Type 'q' to quit
- Follow the instructions for each function

INTELLIGENT MODE (type 'i' to activate):
- draw a heart -> generates a heart
- make a rectangle 10x5 with # -> draws rectangle 10x5 with #
- create a circle with radius 8 -> creates circle with radius 8
- write "HELLO" in ASCII -> converts HELLO to ASCII art
- show examples -> displays the showcase
- surprise me -> generates interesting random art
- help -> shows this help
        """)
    
    def _create_custom_banner(self, text: str, width: int = 50, char: str = '=', 
                                color: Optional[str] = None, border_style: Optional[str] = None) -> str:
        """Create a custom banner with color and border style support."""
        # Get border characters based on style
        if border_style:
            top_char, bottom_char, left_char, right_char = get_border_chars(border_style)
        else:
            top_char = bottom_char = left_char = right_char = char
        
        padding = (width - len(text) - 2) // 2
        border = top_char * width
        lines = [
            border,
            left_char + ' ' * (width - 2) + right_char,
            left_char + ' ' * padding + text + ' ' * (width - padding - len(text) - 2) + right_char,
            left_char + ' ' * (width - 2) + right_char,
            bottom_char * width
        ]
        result = '\n'.join(lines)
        
        # Apply color
        if color:
            color_code = get_color_code(color)
            result = color_code + result + get_color_code('reset')
        
        return result

    def _create_custom_box(self, text: str, border_char: str = '#', 
                           color: Optional[str] = None, border_style: Optional[str] = None) -> str:
        """Create a custom box with color and border style support."""
        # Get border characters based on style
        if border_style:
            top_char, bottom_char, left_char, right_char = get_border_chars(border_style)
        else:
            top_char = bottom_char = left_char = right_char = border_char
        
        lines = text.split('\n')
        width = max(len(line) for line in lines) + 4
        
        border = top_char * width
        result = [border]
        for line in lines:
            padding = width - len(line) - 2
            result.append(left_char + ' ' + line + ' ' * padding + right_char)
        result.append(bottom_char * width)
        
        output = '\n'.join(result)
        
        # Apply color
        if color:
            color_code = get_color_code(color)
            output = color_code + output + get_color_code('reset')
        
        return output

    def _apply_color(self, content: str, color: Optional[str] = None) -> str:
        """Apply color to content if specified."""
        if color:
            # Use smart generator's color mapping which includes light colors
            color_map = {
                'black': '\033[30m',
                'red': '\033[31m',
                'green': '\033[32m',
                'yellow': '\033[33m',
                'blue': '\033[34m',
                'magenta': '\033[35m',
                'cyan': '\033[36m',
                'white': '\033[37m',
                'bright_black': '\033[90m',
                'bright_red': '\033[91m',
                'bright_green': '\033[92m',
                'bright_yellow': '\033[93m',
                'bright_blue': '\033[94m',
                'bright_magenta': '\033[95m',
                'bright_cyan': '\033[96m',
                'bright_white': '\033[97m',
                'light_black': '\033[90m',
                'light_red': '\033[91m',
                'light_green': '\033[92m',
                'light_yellow': '\033[93m',
                'light_blue': '\033[94m',
                'light_magenta': '\033[95m',
                'light_cyan': '\033[96m',
                'light_white': '\033[97m',
                'reset': '\033[0m',
            }
            color_code = color_map.get(color.lower(), '\033[0m')
            return color_code + content + '\033[0m'
        return content
    
    def _print_with_style(self, art: List[str], color: Optional[str], fill_pattern: str, border: str, char: str) -> None:
        """Print art with fill pattern, border, and color styling."""
        if not art:
            print()
            return
        
        # Convert to list if it's a single string
        if isinstance(art, str):
            art = art.split('\n')
        
        # Apply fill pattern if not solid
        if fill_pattern != 'solid' and art:
            height = len(art)
            width = max(len(row) for row in art)
            pattern_grid = apply_fill_pattern(width, height, fill_pattern, char)
            art = pattern_grid
        
        # Apply border if specified
        if border != 'none' and art:
            art = apply_border(art, border, char)
        
        # Apply color
        if color:
            art = [self._apply_color(line, color) for line in art]
        
        # Print the result
        if art:
            print(f"\n{'\n'.join(art)}")
            print()

    def execute_parsed_command(self, command_dict: Dict[str, Any]) -> None:
        """Execute a parsed command dictionary."""
        command = command_dict.get('command', '')
        params = command_dict.get('params', {})
        
        # Handle compound commands
        if command == 'compound':
            parts = command_dict.get('parts', [])
            print(f"\n{Colors.OKBLUE}=== Compound Command ==={Colors.ENDC}")
            for i, part in enumerate(parts, 1):
                print(f"\n{Colors.OKBLUE}[{i}/{len(parts)}]{Colors.ENDC}")
                self.execute_parsed_command(part)
            return
        
        # Handle smart generation commands
        if command in ['smart', 'surprise', 'random', 'interesting', 'amazing', 'minimal', 'complex', 'geometric', 'nature', 'abstract']:
            art = smart_gen.generate_from_command(command)
            print(f"\n{Colors.OKGREEN}{'\n'.join(art)}{Colors.ENDC}")
            return
        
        # Extract style parameters for smart patterns
        fill_pattern = params.get('fill', params.get('pattern', 'solid'))
        border = params.get('border', 'none')
        char = params.get('char', '#')
        color = params.get('color')
        font = params.get('font', 'small')
        border_style = params.get('border_style', border)
        
        # Add new shapes to command mapping
        def render_shape(shape_name, *args):
            shape_func = {
                'rectangle': draw_rectangle,
                'triangle': draw_triangle,
                'circle': draw_circle,
                'heart': draw_heart,
                'diamond': draw_diamond,
                'tree': generate_tree,
                'spiral': generate_spiral,
                'star': draw_star,
                'hexagon': draw_hexagon,
                'oval': draw_oval,
                'arrow': draw_arrow,
                'pentagon': draw_pentagon,
                'butterfly': draw_butterfly,
                'flower': draw_flower,
            }.get(shape_name)
            if shape_func:
                art = shape_func(*args)
                rendered = self._apply_style_to_art(art, params)
                print(f"\n{'\n'.join(rendered)}")
        
        command_mapping = {
            'text_to_ascii': lambda: print(f"\n{self._apply_color(text_to_ascii(params.get('text', 'ASCII'), font), color)}"),
            'rectangle': lambda: render_shape('rectangle', params.get('width', 10), params.get('height', 5), char, params.get('filled', True)),
            'triangle': lambda: render_shape('triangle', params.get('height', 5), char, params.get('direction', 'up')),
            'circle': lambda: render_shape('circle', params.get('radius', 5), char),
            'heart': lambda: render_shape('heart', params.get('size', 2), char),
            'diamond': lambda: render_shape('diamond', params.get('size', 5), char),
            'tree': lambda: render_shape('tree', params.get('height', 5), char),
            'star': lambda: render_shape('star', params.get('size', 5), char),
            'hexagon': lambda: render_shape('hexagon', params.get('size', 5), char),
            'oval': lambda: render_shape('oval', params.get('width', 10), params.get('height', 5), char),
            'arrow': lambda: render_shape('arrow', params.get('direction', 'right'), params.get('size', 5), char),
            'pentagon': lambda: render_shape('pentagon', params.get('size', 5), char),
            'butterfly': lambda: render_shape('butterfly', params.get('size', 5), char),
            'flower': lambda: render_shape('flower', params.get('size', 5), char),
            'gradient': lambda: print(f"\n{self._apply_color(generate_gradient(params.get('width', 10), params.get('height', 5)), color)}"),
            'checkerboard': lambda: print(f"\n{self._apply_color(generate_checkerboard(params.get('size', 8), params.get('chars', '# ')), color)}"),
            'spiral': lambda: render_shape('spiral', params.get('size', 10), char),
            'random_art': lambda: print(f"\n{self._apply_color(random_abstract(params.get('width', 20), params.get('height', 10)), color)}"),
            'random_face': lambda: print(f"\n{self._apply_color(random_face(), color)}"),
            'random_animal': lambda: print(f"\n{self._apply_color(random_animal(), color)}"),
            'random_emoji': lambda: print(f"\n{self._apply_color(random_emoji(), color)}"),
            'banner': lambda: print(f"\n{self._create_custom_banner(params.get('text', 'ASCII'), params.get('width', 50), params.get('char', '='), color, border_style)}"),
            'box': lambda: print(f"\n{self._create_custom_box(params.get('text', 'Hello\\nWorld'), params.get('char', '#'), color, border_style)}"),
            'spinner': lambda: spinner_animation(params.get('duration', 2.0)),
            'progress_bar': lambda: progress_bar(params.get('duration', 3.0)),
            'showcase': self.menu_showcase,
            'help': self.menu_help,
            'quit': lambda: None,
            'specific_animal': lambda: print(f"\n{self._apply_color(self._get_specific_animal_art(params.get('animal', 'crow')), color)}"),
        }
        
        if command in command_mapping:
            command_mapping[command]()
        else:
            print(f"{Colors.FAIL}Command not recognized: {command}{Colors.ENDC}")
    
    def _apply_style_to_art(self, art: List[str], params: Dict[str, Any]) -> List[str]:
        """Apply fill pattern, border, and color to art based on params."""
        if not art:
            return art
        
        fill_pattern = params.get('fill', params.get('pattern', 'solid'))
        border = params.get('border', 'none')
        char = params.get('char', '#')
        color = params.get('color')
        
        # Convert to list if it's a single string
        if isinstance(art, str):
            art = art.split('\n')
        
        # Apply fill pattern if not solid
        if fill_pattern != 'solid' and isinstance(art, list) and art:
            height = len(art)
            width = max(len(row) for row in art)
            pattern_grid = apply_fill_pattern(width, height, fill_pattern, char)
            art = pattern_grid
        
        # Apply border if specified
        if border != 'none' and isinstance(art, list) and art:
            art = apply_border(art, border, char)
        
        # Apply color
        if color and isinstance(art, list):
            art = [self._apply_color(line, color) for line in art]
        
        return art
    
    def run_intelligent_mode(self) -> None:
        """Run the CLI in intelligent mode (natural language)."""
        print(f"\n{Colors.HEADER}")
        print("  _____ _   _ _   _  ____ _____ _____ ____")
        print(" / ____| \\ | | \\ | |/ ___|_   _|_   _|  _ \\")
        print("| |    |  \\| |  \\| | |   | | | | | | | |_) |")
        print("| |___ | |\\  | |\\  | |___| | | | | | |  _ <")
        print(" \\____||_| \\_|_| \\_|\\____|_| |_| |_| |_| \\_\\" + f"{Colors.ENDC}")
        
        print(f"\n{Colors.OKBLUE}=== INTELLIGENT MODE ==={Colors.ENDC}")
        print(f"{Colors.OKBLUE}Type in natural English (e.g., 'draw a heart' or 'make a rectangle 10x5'){Colors.ENDC}")
        print(f"{Colors.OKBLUE}Type 'menu' to return to menu or 'q' to quit.{Colors.ENDC}\n")
        
        while True:
            try:
                user_input = input(f"{Colors.BOLD}What would you like? {Colors.ENDC}").strip()
                
                if not user_input:
                    continue
                
                # Check for mode switch commands
                if user_input.lower() in ['menu', 'm']:
                    print(f"{Colors.OKGREEN}Returning to menu...{Colors.ENDC}")
                    self.intelligent_mode = False
                    break
                
                if user_input.lower() in ['q', 'quit', 'exit']:
                    print(f"\n{Colors.OKGREEN}Goodbye!{Colors.ENDC}")
                    sys.exit(0)
                
                # Parse the command
                parsed = self.parser.parse_command(user_input)
                
                if parsed:
                    command = parsed.get('command')
                    if command == 'quit':
                        print(f"\n{Colors.OKGREEN}Goodbye!{Colors.ENDC}")
                        sys.exit(0)
                    self.execute_parsed_command(parsed)
                    print()  # Add spacing
                else:
                    # Try to give helpful suggestions
                    print(f"{Colors.WARNING}Could not understand. Try this:{Colors.ENDC}")
                    self._suggest_commands(user_input)
                    
            except KeyboardInterrupt:
                print(f"\n{Colors.WARNING}Use 'q' to quit or 'menu' to return to menu.{Colors.ENDC}")
            except Exception as e:
                print(f"{Colors.FAIL}Error: {e}{Colors.ENDC}")
    
    def _suggest_commands(self, user_input: str) -> None:
        """Suggest possible commands based on user input."""
        suggestions = []
        text_lower = user_input.lower()
        
        # Check for known shapes
        for shape_key, synonyms in self.parser.SHAPE_SYNONYMS.items():
            for syn in synonyms:
                if syn.lower() in text_lower:
                    suggestions.append(f"- Try: 'draw a {syn}'")
                    break
        
        # Check for actions
        if any(v in text_lower for v in ['help', '?']):
            suggestions.append("- Type 'help' to see the help")
        
        if any(v in text_lower for v in ['quit', 'exit']):
            suggestions.append("- Type 'q' or 'quit' to exit")
        
        if any(v in text_lower for v in ['menu']):
            suggestions.append("- Type 'menu' to return to main menu")
        
        if not suggestions:
            suggestions = [
                "- Example: 'draw a heart'",
                "- Example: 'make a rectangle 10x5'",
                "- Example: 'write HELLO in ASCII'",
                "- Example: 'show examples'",
                "- Type 'help' to see all options"
            ]
        
        for suggestion in suggestions[:3]:  # Show max 3 suggestions
            print(f"  {suggestion}")
    
    def run(self) -> None:
        """Run the CLI."""
        print(f"\n{Colors.HEADER}")
        print("  _____ _   _ _   _  ____ _____ _____ ____")
        print(" / ____| \\ | | \\ | |/ ___|_   _|_   _|  _ \\")
        print("| |    |  \\| |  \\| | |   | | | | | | | |_) |")
        print("| |___ | |\\  | |\\  | |___| | | | | | |  _ <")
        print(" \\____||_| \\_|_| \\_|\\____|_| |_| |_| |_| \\_\\" + f"{Colors.ENDC}")
        # Check if we should start in intelligent mode
        if self.intelligent_mode:
            self.run_intelligent_mode()
        else:
            self.menu.run()


def main():
    """Main entry point."""
    cli = ASCIIArtCLI()
    cli.run()


if __name__ == "__main__":
    main()
