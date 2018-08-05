# -*- coding: utf-8 -*-

"""
Modulo che ci viene in auto per segnarci tutte le varie query
da utilizzare per i vari test da eseguire per il girolone (il grafico in alto).

NB: Ricordiamoci che i test si basano sui dati inseriti con il populatedb.
Se viene cambiato lui, i test devono essere aggiornati di conseguenza.
"""

chartQuery1 = """
{
  chart(
    startDate: "2017-04-01",
    endDate: "2017-04-16")
  {
    coldChart {
      ranges {
        perfect
        good
        bad
        danger
        critical
      }
      totalCount
      wspsPercentage
    }
    hotChart {
      ranges {
        perfect
        good
        bad
        danger
        critical
      }
      totalCount
      wspsPercentage
    }
  }
}
"""

# Filtriamo per tipo di struttura. In questo caso: torre
chartQuery2 = """
{
  chart(
    startDate: "2017-04-01",
    endDate: "2017-04-16",
    structType: "torre")
  {
    coldChart {
      ranges {
        perfect
        good
        bad
        danger
        critical
      }
      totalCount
      wspsPercentage
    }
    hotChart {
      ranges {
        perfect
        good
        bad
        danger
        critical
      }
      totalCount
      wspsPercentage
    }
  }
}
"""
