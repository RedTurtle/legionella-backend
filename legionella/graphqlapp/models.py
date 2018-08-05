# -*- coding: utf-8 -*-

# Importiamo qui tutti i vari modelli della nostra applicazione in modo
# da poter abilitare l'automatismo della rilevazione delle modifiche
# per le migrazioni (altrimenti makemigrations non trova i modelli).


from .authentication import models
from .building import models
from .floor import models
from .range import models
from .report import models
from .samplerange import models
from .sector import models
from .settings import models
from .structure import models
from .wsp import models
