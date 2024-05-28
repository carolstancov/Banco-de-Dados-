from dataclasses import dataclass, asdict, field, is_dataclass
from random import randint, choice
import random
import string
import uuid
from faker import Faker
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# Conectando ao banco de dados
connStr =  "" # insira aqui a string de conexão
conn = psycopg2.connect(connStr)

# Classes de valores aleatórios e dados de mapeamento
class ValoresAleatorios:
    def id(self):
        return randint(1, 10000)

    def nota_final(self):
        return round(randint(0, 100) / 10, 1)

# Configurando Faker
fake = Faker('pt-BR')
Faker.seed(0)  # Seed para reprodutibilidade

curso_id_map = {
    'Engenharia': 1120,
    'Jornalismo': 1245,
    'Medicina': 1305,
    'Direito': 1459,
    'Administração': 1503,
    'Ciência da Computação': 1678,
    'Odontologia': 1784,
    'Medicina Veterinária': 1890,
    'Estatistica': 1952,
    'Biomedicina': 7414,
    'Fisioterapia': 8741,
    'Psicologia': 5872,
    'Enfermagem': 3654,
    'Relações Públicas': 3170,
    'Arquitetura e Urbanismo': 4961,
    'Publicidade e Propaganda': 2145,
    'Marketing': 5475,
    'Nutrição': 6877
}

departamento_id_map = {
    'Humanidades': 1050,
    'Exatas': 2051,
    'Biológicas': 3052
}

disciplina_id_map = {
    'Matemática': 'MA-01',
    'Biologia': 'BI-10',
    'História': 'HI-25',
    'Química': 'QU-80',
    'Anatomia': 'AN-45',
    'Ética': 'ET-12',
    'Física': 'FI-07'
}


class disciplina:
    aleatorio = ValoresAleatorios()

    id_disciplina: str = ""
    disciplina: str = ""
    id_curso: int = 0
    
    def __init__(self, curso, disciplina):
        self.id_disciplina = uuid.uuid4().hex
        self.disciplina = disciplina
        self.id_curso = curso

@dataclass
class aluno:
    aleatorio = ValoresAleatorios()

    id_aluno: int = field(default_factory=aleatorio.id)
    nome: str = field(default_factory=lambda: fake.first_name() + ' ' + fake.last_name())
    data_entrada: str = field(default_factory=lambda: Faker('pt-BR').date_between(start_date='-4y', end_date='today').strftime('%Y-%m-%d'))
    id_curso: int = field(init=False)

    def __post_init__(self):
        _curso = choice(list(curso_id_map.keys()))
        self.id_curso = curso_id_map.get(_curso, -1)

class curso:
    aleatorio = ValoresAleatorios()

    id_curso: int = field(init=False)
    curso: str = ""
    id_departamento: int = 0

    def __init__(self, curso):
        self.curso = curso

        if self.curso in curso_id_map:
            self.id_curso = curso_id_map[self.curso]
        else:
            self.id_curso = self.aleatorio.id()

        if self.curso in ["Direito", "Administração", "Jornalismo", "Publicidade e Propaganda", "Marketing", "Relações Públicas"]:
            self.departamento = "Humanidades"
        elif self.curso in ["Engenharia", "Ciência da Computação", "Estatistica", "Arquitetura e Urbanismo"]:
            self.departamento = "Exatas"
        elif self.curso in ["Medicina", "Odontologia", "Medicina Veterinária", "Biomedicina", "Fisioterapia", "Psicologia", "Enfermagem", "Nutrição"]:
            self.departamento = "Biológicas"

        self.id_departamento = departamento_id_map[self.departamento]

class departamento:
    aleatorio = ValoresAleatorios()

    id_departamento: int = aleatorio.id()
    departamento: str = ""
    id_chefe: int = 0

    def __init__(self, departamento, chefe):
       self.departamento = departamento
       self.id_departamento = departamento_id_map[departamento]
       self.id_chefe = chefe

@dataclass
class professor:
    aleatorio = ValoresAleatorios()

    id_professor: int = field(default_factory=aleatorio.id)
    nome: str = field(default_factory=lambda: fake.first_name() + ' ' + fake.last_name())
    id_departamento: int = field(init=False)

    def __post_init__(self):
        self.id_departamento = choice(list(departamento_id_map.values()))

class matriz:
    aleatorio = ValoresAleatorios()

    id_matriz: str = 0
    id_curso: int = 0
    id_disciplina: int = 0

    def __init__(self, curso, disc):
        self.id_matriz = uuid.uuid4().hex
        self.id_curso = curso_id_map.get(curso, -1)
        self.id_disciplina = map_curso_disc[self.id_curso][disc]

@dataclass
class historico_disciplina:
    aleatorio = ValoresAleatorios()

    id_disciplina: int = field(default_factory=aleatorio.id)
    id_professor: int = field(default_factory=aleatorio.id)
    semestre: str = field(default_factory=lambda: choice(['1º', '2º', '3º', '4º', '5º', '6º']))
    ano: int = field(default_factory=lambda: randint(2000, 2024))

class historico_escolar:
    aleatorio = ValoresAleatorios()
    
    id_aluno: int = 0
    id_disciplina: str = ""
    semestre: str = ""
    ano: int = 0
    nota_final: float = 0

    def __init__(self, aluno, disciplina):
        self.ano: int = randint(2000, 2024)
        self.semestre: str = choice(['1º', '2º', '3º', '4º', '5º', '6º'])
        self.nota_final: float = self.aleatorio.nota_final()
        self.id_aluno = aluno["id_aluno"]
        
        # Define o ID da disciplina com base no dicionário de mapeamento
        self.id_disciplina = disciplina_id_map.get(disciplina, "GE-11")

@dataclass
class tcc:
    aleatorio = ValoresAleatorios()

    id_grupo: int = field(default_factory=aleatorio.id)
    id_professor: int = field(default_factory=aleatorio.id)
    id_aluno1: int = field(default_factory=aleatorio.id)
    id_aluno2: int = field(default_factory=aleatorio.id)
    id_aluno3: int = field(default_factory=aleatorio.id)

def gera_dataframe_lista_campos_estaticos(cls, n):
    if not is_dataclass(cls):
        raise ValueError(f"{cls} is not a dataclass")

    instance = 0
   
    instance = cls()

    campos_estaticos = {campo: valor for campo, valor in asdict(instance).items() if not callable(valor)}

    data = []
    for i in range(n):
        item = cls()
        data.append({campo: getattr(item, campo) for campo in campos_estaticos})

    return data

# Definir os dataframes

alunos = gera_dataframe_lista_campos_estaticos(aluno, 10)
professores = gera_dataframe_lista_campos_estaticos(professor, 10)
historico_disciplinas = gera_dataframe_lista_campos_estaticos(historico_disciplina, 10)
tccs = gera_dataframe_lista_campos_estaticos(tcc, 10)

# Historico escolar
historico_e = []
for a in alunos:
    for d in disciplina_id_map.keys():
        he = historico_escolar(a, d)
        historico_e.append([he.id_aluno, he.id_disciplina, he.semestre, he.ano, he.nota_final])

# Disciplinas
disciplinas = []
map_curso_disc = {}
for curso_id in curso_id_map.values():
    map_curso_disc[curso_id] = {}
    for disc in disciplina_id_map.keys():
        d = disciplina(curso_id, disc)
        map_curso_disc[curso_id][d.disciplina] = d.id_disciplina
        disciplinas.append([d.id_disciplina, d.disciplina, d.id_curso])

# Corrigir historico escolar
i = 0
for a in alunos:
    for d in disciplina_id_map.keys():
        historico_e[i][1] = map_curso_disc[a["id_curso"]][d]
        i += 1
    
# Corrigir ids da tabela de historico de disciplinas para ids validos
for i in range(10):
    # Pegar uma disciplina aleatoria da lista de disciplinas 
    rand_c = map_curso_disc[choice(list(curso_id_map.values()))]
    rand_d_id = rand_c[choice(list(disciplina_id_map.keys()))]
    historico_disciplinas[i]['id_professor'] = choice(professores)["id_professor"]
    historico_disciplinas[i]['id_disciplina'] = rand_d_id

# Matriz
matriz_curricular = []
for key, value in curso_id_map.items():
    for d in disciplina_id_map.keys():
        m = matriz(key, d)
        matriz_curricular.append([m.id_matriz, m.id_curso, m.id_disciplina])

departamentos = []
for key, value in departamento_id_map.items():
    d = departamento(key, choice(professores)['id_professor'])
    departamentos.append([d.id_departamento, d.departamento, d.id_chefe])

cursos = []
for key, value in curso_id_map.items():
    c = curso(key)
    cursos.append([c.id_curso, c.curso, c.id_departamento])

# Atualizar id_professor no dataframe_tcc com base nos professores
for i in range(len(tccs)):
    tccs[i]["id_professor"] = choice(professores)["id_professor"]
    tccs[i]["id_aluno1"] = choice(alunos)["id_aluno"]
    tccs[i]["id_aluno2"] = choice(alunos)["id_aluno"]
    tccs[i]["id_aluno3"] = choice(alunos)["id_aluno"]

with conn.cursor() as cur:
    # Inserir dataframe_aluno
    alunos_slice = [list(el.values())[0:3] for el in alunos]
    execute_values(cur, "INSERT INTO aluno (id_aluno, nome, data_entrada) VALUES %s ON CONFLICT DO NOTHING", alunos_slice)

    # Inserir dataframe_curso
    cursos_slice = [el[0:2] for el in cursos]
    execute_values(cur, "INSERT INTO curso (id_curso, nome) VALUES %s ON CONFLICT DO NOTHING", cursos_slice)

    # Inserir dataframe_departamento
    departamentos_slice = [el[0:2] for el in departamentos]    
    execute_values(cur, "INSERT INTO departamento (id_departamento, nome) VALUES %s ON CONFLICT DO NOTHING", departamentos_slice)

    # Inserir dataframe_disciplina
    execute_values(cur, "INSERT INTO disciplina (id_disciplina, nome, id_curso) VALUES %s ON CONFLICT DO NOTHING", disciplinas)

    # Inserir dataframe_matriz
    execute_values(cur, "INSERT INTO matriz (id_matriz, id_curso, id_disciplina) VALUES %s ON CONFLICT DO NOTHING", matriz_curricular)

    # Inserir dataframe_professor
    professores_l = [list(el.values()) for el in professores]
    execute_values(cur, "INSERT INTO professor (id_professor, nome, id_departamento) VALUES %s ON CONFLICT DO NOTHING", professores_l)

    #Inserir dataframe_historicoDisciplina
    historico_disciplinas_l = [list(el.values()) for el in historico_disciplinas]
    execute_values(cur, "INSERT INTO historico_disciplina (id_disciplina, id_professor, semestre, ano) VALUES %s ON CONFLICT DO NOTHING", historico_disciplinas_l)

    # Inserir dataframe_historicoEscolar
    execute_values(cur, "INSERT INTO historico_escolar (id_aluno, id_disciplina, semestre, ano, nota_final) VALUES %s ON CONFLICT DO NOTHING", historico_e)

    # Inserir dataframe_tcc
    tccs_l = [list(el.values())[0:5] for el in tccs]
    execute_values(cur, "INSERT INTO tcc (id_grupo, id_professor_orientador, aluno1, aluno2, aluno3) VALUES %s ON CONFLICT DO NOTHING", tccs_l)

    ## ATUALIZAR CHAVES ESTRANGEIRAS

    for a in alunos:
        cur.execute(
            "UPDATE aluno SET id_curso=(%s)"
            " WHERE id_aluno=(%s)",
            (a["id_curso"], a["id_aluno"])
        ) 
    
    for c in cursos:
        cur.execute(
            "UPDATE curso SET id_departamento=(%s)"
            " WHERE id_curso=(%s)",
            (c[2], c[0])
        )

    for d in departamentos:
        cur.execute(
            "UPDATE departamento SET id_chefe=(%s)"
            " WHERE id_departamento=(%s)",
            (d[2], d[0])
        )  
    # Confirmar a transação
    conn.commit()

# Fechar a conexão
conn.close()
