import datetime
from webService import WebService
import Utilidades as ut
import sys

if __name__ == "__main__":
    param = ut.mainMoodle(sys.argv[1:])
    #param = 'moodle_plugin_sessions.txt', '', '2020-08-01 00:00:00,2020-12-31 00:00:00'
    webService = WebService()
    report = []
    ret = 0
    dates = param[2].split(",")
    if param[0] != '' and param[1] == '':
        print("Moodle Sesions...")
        moodlSession = ut.leerUUID(param[0])
        for sesion in moodlSession:
            try:
                nombre_session, date_session = webService.get_moodle_sesion_name(sesion)
            except:
                print('Erro WS')
                nombre_session = None
            if nombre_session == None or nombre_session == ' ':
                print("Session name not found!")
            else:
                print(nombre_session)
                try:
                    lista_grabaciones = webService.get_moodle_lista_grabaciones(nombre_session, dates, date_session)
                except:
                    lista_grabaciones = None
                if lista_grabaciones is None:
                    print("There's no recording for: " + nombre_session)
                else:
                    for grabacion in lista_grabaciones:
                        try:
                            ret = ut.downloadrecording(grabacion['recording_id'],grabacion['recording_name'], dates)
                        except:
                            ret = 2
                        try:
                            if ret == 1:
                                report.append([grabacion['recording_id'], grabacion['recording_name'], grabacion['duration'],
                                               grabacion['storageSize'], grabacion['created']])
                            elif ret == 2:
                                report.append(
                                    ['Erro no download', grabacion['recording_name'], grabacion['duration'],
                                     grabacion['storageSize'], grabacion['created']])
                            elif ret == 3:
                                if [grabacion['recording_id'], grabacion['recording_name'], grabacion['duration'],
                                               grabacion['storageSize'], grabacion['created']] in report:
                                    print("EXISTE")
                                else:
                                    report.append(
                                        [grabacion['recording_id'], grabacion['recording_name'], grabacion['duration'],
                                         grabacion['storageSize'], grabacion['created']])
                        except:
                            print("Nao foi possivel criar o relatorio")

        if len(report) > 0:
            try:
                print(ut.crearReporteMoodle(report, dates))
            except:
                print("Nao foi possivel criar o relatorio")
        else:
            print('No recordings was found')
