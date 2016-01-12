__author__ = 'metallica'


def dame_dietas_pasadas(usuario):
    dietas_pasadas = Dieta.objects.filter(paciente = usuario).filter(status='pasadas')
    return dietas_pasadas

def dame_dieta_vigente(usuario):
    dietas_pasadas = Dieta.objects.filter(paciente = usuario).filter(status='vigente')
    return dietas_pasadas


