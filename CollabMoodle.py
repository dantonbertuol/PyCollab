import datetime
from webService import WebService
import Utilidades as ut
import sys

if __name__ == "__main__":
    param = ut.mainMoodle(sys.argv[1:])
    #param = 'moodle_plugin_sessions.txt', '', '2018-07-01 00:00:00,2018-12-31 00:00:00'
    webService = WebService()
    report = []
    lRet = True
    dates = param[2].split(",")
    if param[0] != '' and param[1] == '':
        print("Moodle Sesions...")
        moodlSession = ut.leerUUID(param[0])
        for sesion in moodlSession:
            nombre_session, date_session = webService.get_moodle_sesion_name(sesion)
            if nombre_session == None or nombre_session == ' ':
                print("Session name not found!")
            else:
                print(nombre_session)
                lista_grabaciones = webService.get_moodle_lista_grabaciones(nombre_session, dates, date_session)
                if lista_grabaciones is None:
                    print("There's no recording for: " + nombre_session)
                else:
                    for grabacion in lista_grabaciones:
                        lRet = ut.downloadrecording(grabacion['recording_id'],grabacion['recording_name'], dates)
                        if lRet:
                            report.append([grabacion['recording_id'], grabacion['recording_name'], grabacion['duration'],
                                           grabacion['storageSize'], grabacion['created']])
                        else:
                            report.append(
                                ['Erro no download', grabacion['recording_name'], grabacion['duration'],
                                 grabacion['storageSize'], grabacion['created']])

        if len(report) > 0:
            print(ut.crearReporteMoodle(report, dates))
        else:
            print('No recordings was found')
    elif param[0] == '' and param[1] != '':
        print("Moodle LTI Integration Download:", param[1])
        moodle_ids = ut.leerUUID(param[1])
        contexto_ids = []
        grabaciones_id = []
        for moodle_id in moodle_ids:
            contexto_id = webService.get_moodle_grabaciones_contexto(moodle_id, tiempo)
            if contexto_id == None:
                print("sessionID no valido")
            else:
                contexto_ids.append(contexto_id)
        for ctx_id in contexto_ids:
            grabacionesIds = webService.get_moodle_grabaciones_id(ctx_id)
            grabaciones = ut.listaGrabaciones(grabacionesIds)
            if grabaciones is None:
                print("There's no recording: " + ctx_id)
            else:
                for grabacion in grabaciones:
                    report.append([grabacion['recording_id'], grabacion['recording_name'], grabacion['duration'],
                                   grabacion['storageSize'], grabacion['created']])
                ut.downloadrecording(grabaciones, ctx_id, ctx_id)
        if len(report) > 0:
            print(ut.crearReporteMoodle(report))
        else:
            print('No recordings was found')
