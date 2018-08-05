# -*- coding: utf-8 -*-

"""
Modulo che ci viene in auto per segnarci tutte le varie mutation
da utilizzare per i vari test da eseguire.

NB: Ricordiamoci che i test si basano sui dati inseriti con il populatedb.
Se viene cambiato lui, i test devono essere aggiornati di conseguenza.
"""

createSamplerange = """
mutation createSamplerange {
  createSamplerange(input: {
    datesList: ["2017-01-09", "2017-01-16"],
    company: "compagnia: attenti!",
    title: "titolo bellisismo",
    description: "descrizione ciaone",
    filterOn: false}) {
            ok
  }
}
"""
