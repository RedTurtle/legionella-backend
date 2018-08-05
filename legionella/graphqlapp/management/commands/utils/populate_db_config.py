# -*- coding: utf-8 -*-

from graphqlapp.building.models import Building
from graphqlapp.floor.models import Floor
from graphqlapp.sector.models import Sector
from graphqlapp.structure.models import Structure
from graphqlapp.range.models import Range
from graphqlapp.report.models import Report
from graphqlapp.samplerange.models import SampleRange
from graphqlapp.document.models import Document
from graphqlapp.settings.models import Settings
from graphqlapp.wsp.models import Wsp

SUBSTATIONS_BUILDINGS = {
    'Sottocentrale 1': ['42', '43', '44'],
    'Sottocentrale 2': ['14', '15', '16', '17', '18', '19', '33'],
    'Sottocentrale 3': ['1', '2', '6', '34', '35', '36', '38'],
    'Sottocentrale 4': ['41', '45', '46'],
    'Sottocentrale 5': ['3', '4', '5', '7', '8', '29', '30', '37', '39'],
    'Sottocentrale 6': ['9', '10', '11', '12', '13', '20', '21', '22', '23',
                        '24', '27', '31', '32'],
}

SECTORS = [
    # ("1E0", "Lab. Ematologia-Fisiopat.Coaugul. - Neurochimica - Farmacia"),
    ("1A0", "Edificio Amministrativo"),
    ("1A1", "Edificio Amministrativo"),
    ("1A2", "Edificio Amministrativo"),
    ("1B0", "Degenza Hospice"),
    ("1B-1", "Spogliatoio Centralizzato Personale"),
    ("1B2", "Degenza Chirurgie Specialistiche"),
    ("2B-1", "Spogliatoio Centralizzato Personale"),
    ("1C-1", "Spogliatoio Centralizzato Personale"),
    ("2C0", "Medicina Nucleare"),
    ("2C1", "Degenza Terapia Radiometabolica"),
    ("1D0", "Radioterapia"),
    ("1D1", "Ambulatori DAI Chirurgico e Ostetricia Ginecologia"),
    ("1E0", "Laboratorio Trasfusionale"),
    ("1E1", "Laboratorio Analisi chimico-cliniche"),
    ("1H-1", "Morgue - sale utoptiche "),
    ("TR1", "Torre di raffreddamento uno"),
    ("TR2", "Torre di raffreddamento due"),
]


CONTENTYPE_PERMISSIONS_FOR_MANAGER = [
    Building,
    Floor,
    Sector,
    Structure,
    Wsp,
    Range,
    Report,
    SampleRange,
    Document,
    Settings,
]

# Questo dizionario permette di specificare a quali tipi di oggetti deve essere
# rimosso il permesso di delete per il gruppo manager.
# Usato in 'create_groups'
MANAGER_CANNOT_DELETE = {
    Wsp: 'delete_wsp',
    Building: 'delete_building',
    Floor: 'delete_floor',
    Structure: 'delete_structure',
    Sector: 'delete_sector',
}

CONTENTYPE_PERMISSIONS_FOR_TECNICO = [
    Report,
    SampleRange,
    Document,
]


LEGIONELLA_TYPES = [
    # ( ceppo, description )
    ('L. adelaidensis', ''),
    ('L. anisa', ''),
    ('L. beliardensis', ''),
    ('L. birminghamensis', ''),
    ('L. bozemanil', '2 siero gruppi'),
    ('L. brunenti', ''),
    ('L. busanensis', ''),
    ('L. cardiaca', ''),
    ('L. cherril', ''),
    ('L. cincinnatiensis', ''),
    ('L. drancourtil', ''),
    ('L. dresdenensis', ''),
    ('L. drozanskil', ''),
    ('L. pneumophila', ''),
]

ALLOWED_FILE_EXT = [
    '.doc',
    '.pdf',
    '.docx',
    '.xls',
    '.xlsx',
    '.odt',
    '.jpg',
    '.jpeg',
]
