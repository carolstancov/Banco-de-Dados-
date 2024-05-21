CREATE TABLE aluno (
	id_aluno int NOT NULL PRIMARY KEY,
	nome varchar,
	data_entrada varchar,
	id_curso int
);

CREATE TABLE curso (
	id_curso int NOT NULL PRIMARY KEY, 
	nome varchar,
	id_departamento int
);

CREATE TABLE professor(
	id_professor int NOT NULL PRIMARY KEY,
	nome varchar, 
	id_departamento int 
);

CREATE TABLE departamento(
	id_departamento int NOT NULL PRIMARY KEY,
	nome varchar,
	id_chefe int
);

CREATE TABLE disciplina(
	id_disciplina varchar NOT NULL PRIMARY KEY, 
	nome varchar,
	id_curso int
);

CREATE TABLE matriz(
	id_matriz varchar NOT NULL PRIMARY KEY, 
	id_curso int, 
	id_disciplina varchar
);

CREATE TABLE tcc(
	id_grupo int NOT NULL PRIMARY KEY,  
	id_professor_orientador int, 
	aluno1 int, 
	aluno2 int, 
	aluno3 int
);

CREATE TABLE historico_escolar(
	id_aluno int, 
	id_disciplina varchar,
	semestre varchar, 
	ano int, 
	nota_final decimal
);

CREATE TABLE historico_disciplina(
	id_disciplina varchar, 
	id_professor int, 
	semestre varchar, 
	ano int
);

ALTER TABLE aluno
ADD CONSTRAINT curso_fk
FOREIGN KEY (id_curso) REFERENCES curso(id_curso);

ALTER TABLE curso 
ADD CONSTRAINT departamento_fk
FOREIGN KEY (id_departamento) REFERENCES departamento(id_departamento); 


ALTER TABLE professor
ADD CONSTRAINT departamento_fk
FOREIGN KEY (id_departamento) REFERENCES departamento(id_departamento);

ALTER TABLE departamento
ADD CONSTRAINT chefe_fk
FOREIGN KEY (id_chefe) REFERENCES professor(id_professor);


ALTER TABLE disciplina 
ADD CONSTRAINT curso_fk
FOREIGN KEY(id_curso) REFERENCES curso(id_curso);

ALTER TABLE matriz
ADD CONSTRAINT curso_fk
FOREIGN KEY(id_curso) REFERENCES curso(id_curso);

ALTER TABLE matriz 
ADD CONSTRAINT disciplina_fk
FOREIGN KEY(id_disciplina) REFERENCES disciplina(id_disciplina); 

ALTER TABLE tcc
ADD CONSTRAINT professor_orientador_fk
FOREIGN KEY(id_professor_orientador) REFERENCES professor(id_professor);

ALTER TABLE tcc 
ADD CONSTRAINT aluno1_fk
FOREIGN KEY(aluno1) REFERENCES aluno(id_aluno); 

ALTER TABLE tcc 
ADD CONSTRAINT aluno2_fk
FOREIGN KEY(aluno2) REFERENCES aluno(id_aluno); 

ALTER TABLE tcc 
ADD CONSTRAINT aluno3_fk
FOREIGN KEY(aluno3) REFERENCES aluno(id_aluno); 

ALTER TABLE historico_escolar
ADD CONSTRAINT aluno_fk
FOREIGN KEY(id_aluno) REFERENCES aluno(id_aluno); 

ALTER TABLE historico_escolar
ADD CONSTRAINT disciplina_fk
FOREIGN KEY(id_disciplina) REFERENCES disciplina(id_disciplina);


ALTER TABLE historico_disciplina
ADD CONSTRAINT professor_fk
FOREIGN KEY(id_professor) REFERENCES professor(id_professor);

ALTER TABLE historico_disciplina
ADD CONSTRAINT disciplina_fk 
FOREIGN KEY(id_disciplina) REFERENCES disciplina(id_disciplina);
















