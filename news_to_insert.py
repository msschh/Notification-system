from datetime import datetime

# datetime constructor: datetime(year, month, day, hour=0, minute=0)
news = [
            {
                'text': 'Examenele pentru anii terminali sunt in mai!',
                'now': datetime(2017,10,1,12,0),
                'start': datetime(2018,5,14,0,0),
                'end': datetime(2018,5,27,23,59),
                'author': 'conducereauniversitatii@unibuc.ro',
                'groups': [311,312,313,331,332,333,334,341,342,343,344]
            },
            {
                'text': 'Inscrierea la examenul de licenta se face doar de catre studentii absolventi!',
                'now': datetime(2018,5,1,12,0),
                'start': datetime(2018,6,18,8,0),
                'end': datetime(2018,6,22,18,0),
                'author': 'secretariat@fmi.unibuc.ro',
                'groups': [311,312,313,331,332,333,334,341,342,343,344]
            },
            {
                'text': 'Decontarea abonamentelor RATB: de la 10 la 14!',
                'now': datetime(2018,5,12,8,0),
                'start': datetime(2018,5,15,10,0),
                'end': datetime(2018,5,17,14,0),
                'author': 'contabilitate@fmi.unibuc.ro',
                'groups': [311,312,313,331,332,333,334,341,342,343,344,112,113,134,144,152]
            },
            {
                'text': 'In saptamana 10, cursurile si seminariile de IA nu se vor tine! Vor fi recuperate ulterior',
                'now': datetime(2018,2,18,10,0),
                'start': datetime(2018,5,1,8,0),
                'end': datetime(2018,5,6,0,0),
                'author': 'profesorIA@fmi.unibuc.ro',
                'groups': [241,242,243,244]
            }
       ]

       
            # {
            #  'text': ,
            #  'now': ,
            #  'start': ,
            #  'end': ,
            #  'author': ,
            #  'groups': 
            # }