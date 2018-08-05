# -*- coding: utf-8 -*-

"""
Modulo che ci viene in auto per segnarci tutte le varie query
da utilizzare per i vari test da eseguire.

NB: Ricordiamoci che i test si basano sui dati inseriti con il populatedb.
Se viene cambiato lui, i test devono essere aggiornati di conseguenza.
"""


allSampleranges = """
{
    allSampleranges {
        edges {
            node {
                title
            }
        }
    }
}
"""

firstTwoSampleRanges = """
{
    allSampleranges (first: 2) {
        edges {
            node {
                title
            }
        }
    }
}
"""

allStructure = """
{
  allStructure {
    edges {
      node {
        label
      }
    }
  }
}
"""

allSettings = """
{
  settings {
    edges {
      node {
        settingType
      }
    }
  }
}
"""

reportForSampleRange = """
{
  allSampleranges(first: 2) {
    edges {
      node {
        title
        company
        reportSet {
          edges {
            node {
              id
            }
          }
        }
      }
    }
  }
}
"""
