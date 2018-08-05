# -*- coding: utf-8 -*-

from django.db.models import Q
from django.utils.timezone import utc
from graphqlapp.building.models import Building
from graphqlapp.floor.models import Floor
from graphqlapp.sector.models import Sector
from graphqlapp.settings.models import Settings
from graphqlapp.structure.models import Structure
from graphqlapp.wsp.models import Wsp
import datetime


def create_wsps(self):
    """ This function creates some WSPs.
    """

    if self.flush:
        allWsps = Wsp.objects.all()
        for wsp in allWsps:
            wsp.delete()

    # self.stdout.write("Creating WSP no. 1 [real data]")
    # Riferimento:
    # file "LAST_REGISTRO Misure Temperature - Biossido -LEGIONELLA_2017_Company1+CSTA_31012017.xls"  # noqa
    # foglio: PUNTI WSP nov-dic2016, riga 9
    # foglio: CAMPIONAMENTI 1* TRIM 2017, riga 5

    # wsp per Torre di raffreddamento 1
    nuovowsp = Wsp(
        code="T1.1",
        old_name="4.1",

        structure=Structure.objects.get(
            label="Torre di raffreddamento 1"),
        building=Building.objects.get(label="43"),
        floor=Floor.objects.get(label="0"),

        description="wsp Torre di raffreddamento 1",
        closed_rooms="0",
        open_rooms="0",

        # risk_threshold='',
        risk_level=Settings.objects.get(
            Q(setting_type='risk_level'),
            Q(value='basso')
        ),

        start_date=datetime.date(2017, 1, 1),
        obsolence_date=datetime.date(2017, 12, 1),
        operative_status=True,
        cold=False,
        cold_flow=True,
        hot=True,
        hot_flow=True,
    )
    nuovowsp.save()
    nuovowsp.sector.add(Sector.objects.get(label="TR1"))

    # nuovo wsp per ingresso
    # dati quasi del tutto reali
    # Riferimento:
    # file "LAST_REGISTRO Misure Temperature - Biossido -LEGIONELLA_2017_Company1+CSTA_31012017.xls"  # noqa
    # foglio: PUNTI WSP nov-dic2016, riga 25
    # foglio: CAMPIONAMENTI 1* TRIM 2017, riga 21 (il nome del WSP è una 'i')
    nuovowsp = Wsp(
        code="I1",
        old_name="F1",

        structure=Structure.objects.get(
            label="Ingresso 1"),
        building=Building.objects.get(label="43"),
        floor=Floor.objects.get(label="0"),

        description="Dopo il contatore HERA - ESTERNO",
        closed_rooms="0",
        open_rooms="0",

        # risk_threshold='',
        risk_level=Settings.objects.get(
            Q(setting_type='risk_level'),
            Q(value='basso')
        ),

        start_date=datetime.date(2017, 1, 1),
        obsolence_date=datetime.date(2017, 12, 1),
        operative_status=True,
        cold=False,
        cold_flow=True,
        hot=False,
        hot_flow=False,
    )
    nuovowsp.save()
    nuovowsp.sector.add(Sector.objects.get(label="1C-1"))

    # nuovo WSP: real data
    nuovowsp = Wsp(
        code="3.9.b",
        old_name="57.b",

        structure=Structure.objects.get(
            label="Sottocentrale 3"),
        building=Building.objects.get(label="38"),
        floor=Floor.objects.get(label="2"),

        description="LAVANDINO / BIDET - Servizio igienico stanza di "
                    "degenza - 2.38.22",
        closed_rooms="0",
        open_rooms="23",

        # risk_threshold='',
        risk_level=Settings.objects.get(
            Q(setting_type='risk_level'),
            Q(value='medio')
        ),

        start_date=datetime.date(2017, 3, 1),
        obsolence_date=datetime.date(2017, 11, 1),
        operative_status=True,
        cold=False,
        cold_flow=False,
        hot=True,
        hot_flow=True,
    )
    nuovowsp.save()
    nuovowsp.sector.add(Sector.objects.get(label="1B2"))

    # nuovo WSP: real data
    nuovowsp = Wsp(
        code="4.2",
        old_name="44",

        structure=Structure.objects.get(
            label="Sottocentrale 4"),
        building=Building.objects.get(label="41"),
        floor=Floor.objects.get(label="1"),

        description="LAVELLO - Cucinetta - 1.41.22B",
        closed_rooms="0",
        open_rooms="0",

        # risk_threshold='',
        risk_level=Settings.objects.get(
            Q(setting_type='risk_level'),
            Q(value='basso')
        ),

        start_date=datetime.date(2017, 2, 1),
        obsolence_date=datetime.date(2017, 10, 1),
        operative_status=True,
        cold=True,
        cold_flow=True,
        hot=False,
        hot_flow=False,
    )
    nuovowsp.save()
    nuovowsp.sector.add(Sector.objects.get(label="1A1"))

    # nuovo WSP: real data
    # Riferimento:
    # file "LAST_REGISTRO Misure Temperature - Biossido -LEGIONELLA_2017_Company1+CSTA_31012017.xls"  # noqa
    # foglio: PUNTI WSP nov-dic2016, riga 44
    # foglio: CAMPIONAMENTI 1* TRIM 2017, riga 40
    nuovowsp = Wsp(
        code="1.4",
        old_name="69",

        structure=Structure.objects.get(
            label="Sottocentrale 1"),
        building=Building.objects.get(label="42"),
        floor=Floor.objects.get(label="-1"),

        description="LAVANDINO - SALA AUTOPTICA S.42.11",
        closed_rooms="0",
        open_rooms="0",

        # risk_threshold='',
        risk_level=Settings.objects.get(
            Q(setting_type='risk_level'),
            Q(value='basso')
        ),

        start_date=datetime.date(2015, 8, 16),
        obsolence_date=datetime.date(2017, 11, 11),
        operative_status=True,
        cold=False,
        cold_flow=True,
        hot=True,
        hot_flow=True,
    )
    nuovowsp.save()
    nuovowsp.sector.add(Sector.objects.get(label="1H-1"))

    # wsp per Torre di raffreddamento 2 (dati inventati)
    nuovowsp = Wsp(
        code="T2.2",
        old_name="5.2",

        structure=Structure.objects.get(
            label="Torre di raffreddamento 2"),
        building=Building.objects.get(label="1"),
        floor=Floor.objects.get(label="0"),

        description="wsp nella Torre di raffreddamento 2",
        closed_rooms="5",
        open_rooms="1",

        # risk_threshold='',
        risk_level=Settings.objects.get(
            Q(setting_type='risk_level'),
            Q(value='medio')
        ),

        start_date=datetime.datetime.strptime(
            '2017-02-01T01:01', '%Y-%m-%dT%H:%M'
        ).replace(tzinfo=utc),
        obsolence_date=datetime.datetime.strptime(
            '2018-12-01T01:01', '%Y-%m-%dT%H:%M'
        ).replace(tzinfo=utc),
        operative_status=True,
        cold=False,
        cold_flow=True,
        hot=True,
        hot_flow=False,
    )
    nuovowsp.save()
    nuovowsp.sector.add(Sector.objects.get(label="1B-1"))

    nuovowsp = Wsp(
        code="T1.3",
        old_name="4.3",

        structure=Structure.objects.get(
            label="Torre di raffreddamento 1"),
        building=Building.objects.get(label="1"),
        floor=Floor.objects.get(label="0"),
        # sector=Sector.objects.get(label="TR1"),

        description="wsp 3 Torre di raffreddamento 1",
        closed_rooms="0",
        open_rooms="0",

        # risk_threshold='',
        risk_level=Settings.objects.get(
            Q(setting_type='risk_level'),
            Q(value='medio')
        ),

        start_date=datetime.datetime.strptime(
            '2017-01-01T01:01', '%Y-%m-%dT%H:%M'
        ).replace(tzinfo=utc),
        obsolence_date=datetime.datetime.strptime(
            '2017-12-01T01:01', '%Y-%m-%dT%H:%M'
        ).replace(tzinfo=utc),
        operative_status=True,
        cold=False,
        cold_flow=True,
        hot=True,
        hot_flow=True,
    )
    nuovowsp.save()
    nuovowsp.sector.add(Sector.objects.get(label="1B-1"))

    nuovowsp = Wsp(
        code="T1.4",
        old_name="4.4",

        structure=Structure.objects.get(
            label="Torre di raffreddamento 1"),
        building=Building.objects.get(label="1"),
        floor=Floor.objects.get(label="0"),
        # sector=Sector.objects.get(label="TR1"),

        description="wsp nella Torre di raffreddamento 1",
        closed_rooms="0",
        open_rooms="0",

        # risk_threshold='',
        risk_level=Settings.objects.get(
            Q(setting_type='risk_level'),
            Q(value='medio')
        ),

        start_date=datetime.datetime.strptime(
            '2017-01-01T01:01', '%Y-%m-%dT%H:%M'
        ).replace(tzinfo=utc),
        obsolence_date=datetime.datetime.strptime(
            '2017-12-01T01:01', '%Y-%m-%dT%H:%M'
        ).replace(tzinfo=utc),
        operative_status=True,
        cold=False,
        cold_flow=True,
        hot=True,
        hot_flow=True,
    )
    nuovowsp.save()
    nuovowsp.sector.add(Sector.objects.get(label="1B-1"))

    # wsp per la Torre di raffreddamento 2
    nuovowsp = Wsp(
        code="1T2",
        old_name="4.1",
        structure=Structure.objects.get(
            label="Torre di raffreddamento 2"),
        building=Building.objects.get(label="1"),
        floor=Floor.objects.get(label="0"),
        # sector=Sector.objects.get(label="TR1"),

        description="wsp 1 Torre di raffreddamento 2",
        closed_rooms="0",
        open_rooms="0",

        # risk_threshold='',
        risk_level=Settings.objects.get(
            Q(setting_type='risk_level'),
            Q(value='medio')
        ),

        start_date=datetime.datetime.strptime(
            '2017-01-01T01:01', '%Y-%m-%dT%H:%M'
        ).replace(tzinfo=utc),
        obsolence_date=datetime.datetime.strptime(
            '2017-12-01T01:01', '%Y-%m-%dT%H:%M'
        ).replace(tzinfo=utc),
        operative_status=True,
        cold=False,
        cold_flow=True,
        hot=True,
        hot_flow=False,
    )
    nuovowsp.save()
    nuovowsp.sector.add(Sector.objects.get(label="TR2"))

    nuovowsp = Wsp(
        code="2T2",
        old_name="4.2",
        structure=Structure.objects.get(
            label="Torre di raffreddamento 2"),
        building=Building.objects.get(label="1"),
        floor=Floor.objects.get(label="0"),
        # sector=Sector.objects.get(label="TR1"),

        description="wsp 2 Torre di raffreddamento 2",
        closed_rooms="0",
        open_rooms="0",

        # risk_threshold='',
        risk_level=Settings.objects.get(
            Q(setting_type='risk_level'),
            Q(value='medio')
        ),

        start_date=datetime.datetime.strptime(
            '2017-01-01T01:01', '%Y-%m-%dT%H:%M'
        ).replace(tzinfo=utc),
        obsolence_date=datetime.datetime.strptime(
            '2017-12-01T01:01', '%Y-%m-%dT%H:%M'
        ).replace(tzinfo=utc),
        operative_status=False,
        cold=True,
        cold_flow=True,
        hot=True,
        hot_flow=False,
    )
    nuovowsp.save()
    nuovowsp.sector.add(Sector.objects.get(label="TR2"))

    nuovowsp = Wsp(
        code="3T2",
        old_name="4.3",
        structure=Structure.objects.get(
            label="Torre di raffreddamento 2"),
        building=Building.objects.get(label="1"),
        floor=Floor.objects.get(label="0"),
        # sector=Sector.objects.get(label="TR1"),

        description="wsp 3 Torre di raffreddamento 2",
        closed_rooms="0",
        open_rooms="0",

        # risk_threshold='',
        risk_level=Settings.objects.get(
            Q(setting_type='risk_level'),
            Q(value='medio')
        ),

        start_date=datetime.datetime.strptime(
            '2017-01-01T01:01', '%Y-%m-%dT%H:%M'
        ).replace(tzinfo=utc),
        obsolence_date=datetime.datetime.strptime(
            '2017-12-01T01:01', '%Y-%m-%dT%H:%M'
        ).replace(tzinfo=utc),
        operative_status=True,
        cold=False,
        cold_flow=True,
        hot=True,
        hot_flow=False,
    )
    nuovowsp.save()
    nuovowsp.sector.add(Sector.objects.get(label="TR2"))

    nuovowsp = Wsp(
        code="4T2",
        old_name="4.4",
        structure=Structure.objects.get(
            label="Torre di raffreddamento 2"),
        building=Building.objects.get(label="1"),
        floor=Floor.objects.get(label="0"),

        description="wsp 4 Torre di raffreddamento 2",
        closed_rooms="0",
        open_rooms="0",

        # risk_threshold='',
        risk_level=Settings.objects.get(
            Q(setting_type='risk_level'),
            Q(value='alto')
        ),

        start_date=datetime.datetime.strptime(
            '2017-01-01T01:01', '%Y-%m-%dT%H:%M'
        ).replace(tzinfo=utc),
        obsolence_date=datetime.datetime.strptime(
            '2017-12-01T01:01', '%Y-%m-%dT%H:%M'
        ).replace(tzinfo=utc),
        operative_status=True,
        cold=False,
        cold_flow=False,
        hot=False,
        hot_flow=True,
    )
    nuovowsp.save()
    nuovowsp.sector.add(Sector.objects.get(label="TR2"))

    # wsp per sottocentrale 2
    nuovowsp = Wsp(
        code="2.1",
        old_name="21",
        structure=Structure.objects.get(
            label="Sottocentrale 2"),
        building=Building.objects.get(label="41"),
        floor=Floor.objects.get(label="1"),
        # sector=Sector.objects.get(label="1A1"),

        description="un wsp nella sottocentrale 2",
        closed_rooms="0",
        open_rooms="0",

        # risk_threshold='',
        risk_level=Settings.objects.get(
            Q(setting_type='risk_level'),
            Q(value='basso')
        ),

        start_date=datetime.date(2017, 02, 01),
        obsolence_date=datetime.datetime.strptime(
            '2017-10-01T01:01', '%Y-%m-%dT%H:%M'
        ).replace(tzinfo=utc),
        operative_status=True,
        cold=True,
        cold_flow=True,
        hot=True,
        hot_flow=True,
    )
    nuovowsp.save()
    nuovowsp.sector.add(Sector.objects.get(label="1D0"))

    nuovowsp = Wsp(
        code="2.2",
        old_name="22",
        structure=Structure.objects.get(
            label="Sottocentrale 4"),
        building=Building.objects.get(label="41"),
        floor=Floor.objects.get(label="1"),
        # sector=Sector.objects.get(label="1A1"),

        description="wsp 2 Sottocentrale 4",
        closed_rooms="0",
        open_rooms="0",

        # risk_threshold='',
        risk_level=Settings.objects.get(
            Q(setting_type='risk_level'),
            Q(value='basso')
        ),

        start_date=datetime.date(2017, 02, 01),
        obsolence_date=datetime.datetime.strptime(
            '2017-10-01T01:01', '%Y-%m-%dT%H:%M'
        ).replace(tzinfo=utc),
        operative_status=True,
        cold=True,
        cold_flow=True,
        hot=True,
        hot_flow=True,
    )
    nuovowsp.save()
    nuovowsp.sector.add(Sector.objects.get(label="1H-1"))

    # wsp per INGRESSO (dati inventati)
    nuovowsp = Wsp(
        code="7.8",
        old_name="56",
        structure=Structure.objects.get(
            label="Ingresso 1"),
        building=Building.objects.get(label="41"),
        floor=Floor.objects.get(label="1"),
        # sector=Sector.objects.get(label="1A1"),

        description="Wsp ingresso 1",
        closed_rooms="0",
        open_rooms="0",

        # risk_threshold='',
        risk_level=Settings.objects.get(
            Q(setting_type='risk_level'),
            Q(value='basso')
        ),

        start_date=datetime.date(2017, 02, 01),
        obsolence_date=datetime.datetime.strptime(
            '2017-10-01T01:01', '%Y-%m-%dT%H:%M'
        ).replace(tzinfo=utc),
        operative_status=True,
        cold=True,
        cold_flow=True,
        hot=True,
        hot_flow=True,
    )
    nuovowsp.save()
    nuovowsp.sector.add(Sector.objects.get(label="2C0"))

    nuovowsp = Wsp(
        code="7.9",
        old_name="57",
        structure=Structure.objects.get(
            label="Ingresso 1"),
        building=Building.objects.get(label="41"),
        floor=Floor.objects.get(label="1"),
        # sector=Sector.objects.get(label="1A1"),

        description="Wsp 2 ingresso 1",
        closed_rooms="0",
        open_rooms="0",

        # risk_threshold='',
        risk_level=Settings.objects.get(
            Q(setting_type='risk_level'),
            Q(value='basso')
        ),

        start_date=datetime.date(2017, 02, 01),
        obsolence_date=datetime.datetime.strptime(
            '2017-10-01T01:01', '%Y-%m-%dT%H:%M'
        ).replace(tzinfo=utc),
        operative_status=True,
        cold=True,
        cold_flow=True,
        hot=True,
        hot_flow=True,
    )
    nuovowsp.save()
    nuovowsp.sector.add(Sector.objects.get(label="1E0"))
