from flask import *
from .user import is_logged

main = Blueprint('main', __name__)

@main.get('/class')
def class_screen():
    if is_logged():
        class_id = request.args.get('class_id')
        # adicionar verificação da validade do acesso à turma
        # separar as rotas do aluno e do professor

        class_data = {
            'class_id': 'CLASS_TEST_ID',
            'name': 'Turma de Teste',
            'description': 'Turma de Teste',
            'professor': ['Marsio', 'Pedro'],
            'students': ['Carlos', 'Frederico'],
            'lessons' : [
                { 'name': 'Aula 1', 'id' : '1'},
                { 'name': 'Aula 2', 'id' : '2'},
                ]
            }
        
        return render_template("class_professor.jinja", class_data=class_data)
    else:
        return redirect("/")
    
@main.get('/class/stats')
def class_stats():
    if is_logged():
        class_id = request.args.get('class_id')
        # adicionar verificação da validade do acesso à turma como professor

        class_data = {
            'class_id': '1',
            'name': 'Turma de Teste',
            'description': 'Turma de Teste',
            'professor': ['Marsio', 'Pedro'],
            'students': ['Carlos', 'Frederico'],
            'lessons' : [
                { 'name': 'Aula 1', 'id' : '1'},
                { 'name': 'Aula 2', 'id' : '2'},
                ]
            }
        # adicionar verificação da validade do acesso à turma
        return render_template("class_stats.jinja", class_data=class_data)
    else:
        return redirect("/")

@main.get('/lesson')
def lesson_screen():
    if is_logged():
        lesson_id = request.args.get('lesson_id')
        # adicionar verificação da validade do acesso à aula

        lesson_data = {
            'lesson_id': '1',
            'name': 'Aula 1',
            'description': 'Aula de Teste',
            'content': 'Conteúdo da Aula',
            'class_id': 'CLASS_TEST_ID'
            }
        
        return render_template("lesson.jinja", lesson_data=lesson_data)
    else:
        return redirect("/")
