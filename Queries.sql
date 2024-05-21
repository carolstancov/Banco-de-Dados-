--1 - historico escolar
select d.id_disciplina, d.nome, h.semestre, h.ano, h.nota_final 
from disciplina as d
right join historico_escolar as h
	on d.id_disciplina = h.id_disciplina
where id_aluno = 1702 --id do aluno 


-- 2. - historico de disciplina

select * from historico_disciplina hd
where hd.id_professor = 485


--3 - alunos formados 


select a.nome,a.id_aluno, m.id_curso, m.id_disciplina
from aluno as a
left join matriz m
	on a.id_curso = m.id_curso
left join historico_escolar he
	on he.id_disciplina = m.id_disciplina
	and a.id_aluno = he.id_aluno 
where 
	he.ano = 2013
	and he.semestre = 3
	

-- 4 - professores 

select p.id_professor, p.nome, d.nome
from professor as p
right join departamento as d 
	on p.id_professor = d.id_chefe

-- 5 - tcc 
	
select gt.id_grupo, a.nome, p.nome 
from aluno as a
right join tcc as gt
	on id_aluno = gt.aluno1
	or id_aluno = gt.aluno2
	or id_aluno = gt.aluno3
right join professor as p
	on p.id_professor = gt.id_professor_orientador 
where a.nome is not null