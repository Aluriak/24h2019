"""Transcript of emotions in colors.

Emotions are found via IRC bot.

"""

import random
import irc.bot
import irc.strings
import irc.client
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import utils
from laumio import Laumio

# laumios = list(Laumio.init_all(servername='localhost'))
laumios = list(Laumio.init_all(servername='mpd.lan'))

def sentiments_from(sentence):
    analyzer = SentimentIntensityAnalyzer()
    return analyzer.polarity_scores(sentence)


class Bot(irc.bot.SingleServerIRCBot):
    """IRC bot that will get sentences from"""

    def __init__(self):
        super().__init__([('irc.freenode.net', 6667)],
                         'jean-charles-le-garde-bois', 'jean-charles-le-garde-bois')

    @utils.crash_on_error
    def do_command(self, message:str):
        sentiments = sentiments_from(message)
        negativ = sentiments['neg']
        positiv = sentiments['pos']
        neutral = sentiments['neu']
        compound = sentiments['compound']
        nb_laumio = len(laumios)
        nb_negativ_laumios = int(round(negativ * nb_laumio, 0))
        nb_positiv_laumios = int(round(positiv * nb_laumio, 0))
        nb_neutral_laumios = int(round(neutral * nb_laumio, 0))
        print(negativ, positiv, neutral, compound)
        print(nb_negativ_laumios, nb_positiv_laumios, nb_neutral_laumios)
        assert nb_negativ_laumios + nb_positiv_laumios + nb_neutral_laumios == nb_laumio
        random.shuffle(laumios)
        negativ_laumios = laumios[:nb_negativ_laumios]
        positiv_laumios = laumios[nb_negativ_laumios:nb_negativ_laumios+nb_positiv_laumios]
        neutral_laumios = laumios[nb_negativ_laumios+nb_positiv_laumios:]
        for laumio in negativ_laumios:
            laumio.fill('red')
        for laumio in positiv_laumios:
            laumio.fill('green')
        for laumio in neutral_laumios:
            laumio.fill('white')
        # switchs some rings according to compounds
        non_empty_sets = tuple(s for s in (negativ_laumios, positiv_laumios, neutral_laumios) if s)
        while random.random() < (1-abs(compound)) and len(non_empty_sets) > 1:
            one, two = map(random.choice, random.sample(non_empty_sets, 2))
            one_ring = random.randint(0, 2)
            two_ring = random.randint(0, 2)
            if one in negativ_laumios: one_color = 'red'
            if one in positiv_laumios: one_color = 'green'
            if one in neutral_laumios: one_color = 'white'
            if two in negativ_laumios: two_color = 'red'
            if two in positiv_laumios: two_color = 'green'
            if two in neutral_laumios: two_color = 'white'
            # exchange the two colors
            print(f'EXCHANGE: {one}/{one_ring}/{one_color} with {two}/{two_ring}/{two_color}')
            one.set_ring(one_ring, two_color)
            two.set_ring(two_ring, one_color)



    def on_nicknameinuse(self, c, e):
        """If nickname already used, add _ at the end and go on"""
        self.nickname = self.nickname + '_'
        c.nick(self.nickname)

    def on_welcome(self, c, e):
        """When connected to server, join targeted channel"""
        # c.join('#24hc19')
        c.join('#babbage_collectors_24h')
        self.connection = c
        print('JOINING…')

    def on_pubmsg(self, c, e):
        """Call plugin if message is a command message"""
        assert(c == self.connection)
        print('ARG:', e.arguments[0])
        message = e.arguments[0]
        self.do_command(message)


if __name__ == '__main__':
    Bot().start()
