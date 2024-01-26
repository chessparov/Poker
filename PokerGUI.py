import sys
import ctypes
import copy
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

import Poker_TCard
import Poker_THand
import Poker_TStdDeck
import Poker_Exceptions
import Poker_HandCheck
import Poker_PreFlopOdds
import Poker_FlopOdds
import Poker_TurnOdds


myappid = 'poker.solutions.0.1'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class TexceptionDialog(QDialog):

    def __init__(self, exception: str):
        super().__init__()
        self.setGeometry(500, 300, 200, 120)
        self.setWindowIcon(QtGui.QIcon('Assets/Exception_x.png'))
        self.setWindowTitle('Error')
        layout = QVBoxLayout()
        label = QLabel(exception)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.setCenterButtons(True)
        layout.addWidget(self.buttonBox)
        # layout.setAlignment(Qt.AlignRight)
        self.setFont(QFont("Segoe UI", 11))
        self.setLayout(layout)

        self.quitSc = QShortcut(QKeySequence('Return'), self)
        self.quitSc.activated.connect(self.clickMethod)

class TsubHelpWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 800)
        self.setWindowIcon(QtGui.QIcon('Assets/Excl_mark.jpg'))
        self.setWindowTitle('Help')

class TsubWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setGeometry(900, 100, 700, 400)
        self.setWindowIcon(QtGui.QIcon('Assets/Spades.png'))

class TmainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.help = None
        self.w = None
        self.deck = Poker_TStdDeck.TStdDeck()
        self.hand = Poker_THand.THand(self.deck, 2)
        self.input_counter = int(0)
        self.input_dict = {0: 'first', 1: 'second', 2: 'third', 3: 'fourth', 4: 'fifth', 5: 'sixth', 6: 'seventh', 7: ''}
        self.initUI()
        self.setGeometry(200, 100, 600, 600)
        self.setWindowTitle("Texas Hold'em Hand Analysis")
        self.setWindowIcon(QtGui.QIcon('../Poker/Assets/Spades.png'))


        self.setInput()



    def initUI(self):

        QtGui.QFontDatabase.addApplicationFont(r"/Azonix.otf")
        title = QLabel(self)
        title.setText("Welcome\n\nto\n\nTexas Hold'em Hand Analysis")
        title.move(50, 0)
        title.setAlignment(Qt.AlignCenter)
        sansFont = QFont("Azonix", 20)
        title.setFont(sansFont)
        title.setFixedSize(500, 200)

        layout = QVBoxLayout()
        layout.addWidget(title)
        self.setLayout(layout)


    def setInput(self):

        box_label = QLabel(self)
        box_label.setText('Type your cards in the box below and press enter to submit.')
        box_label.move(50, 240)
        box_label.setFixedSize(500, 40)
        box_label.setFont(QFont("Segoe UI", 12))
        box_label.setAlignment(Qt.AlignCenter)

        self.input = QLineEdit(self)
        self.input.move(140, 285)
        self.input.setPlaceholderText(f'Insert your {self.input_dict[self.input_counter]} card (e.g. jh)')
        self.input.setFont(QFont("Segoe UI", 11))
        self.input.resize(320, 32)

        enter_button = QPushButton('OK', self)
        enter_button.setAutoDefault(True)
        enter_button.setDefault(True)
        enter_button.clicked.connect(self.clickMethod)
        enter_button.resize(322, 30)
        enter_button.move(139, 320)

        restart_button = QPushButton('Restart', self)
        restart_button.clicked.connect(self.restartMethod)
        restart_button.resize(322, 30)
        restart_button.move(139, 352)

        self.quitSc = QShortcut(QKeySequence('Return'), self)
        self.quitSc.activated.connect(self.clickMethod)

    def clickMethod(self):
        if self.input_counter == 0:
            self.hand.hand = list()
            self.hand.pocket = list()
            self.hand.table = list()
            self.hand.deckcopy = copy.deepcopy(self.deck)

        self.input_counter += 1
        if self.input.text() == '?':
            if self.help is None:
                self.help = TsubWindow()
                layout = QVBoxLayout()
                help_label = QLabel(help(Poker_TCard.TCard))
                help_label.setAlignment(Qt.AlignLeft)
                layout.addWidget(help_label)
                self.help.setLayout(layout)
                self.help.show()
            else:
                self.help.close()
                self.help = None
            self.input_counter -= 1

        try:
            card = Poker_TCard.TCard(self.input.text())
            if card.getName() in self.hand.deck.getCardNames():
                if card.getName() in self.hand.deckcopy.getCardNames():
                    self.hand.deckcopy.removeCard(card)
                    self.hand.hand.append(card)
                    if len(self.hand.pocket) < 2:
                        self.hand.pocket.append(card)
                    else:
                        self.hand.table.append(card)
                    self.showCardsMethod()

                else:
                    raise Poker_Exceptions.ExceptCardExist
            else:
                raise Poker_Exceptions.ExceptInvalidCard

        except Poker_Exceptions.ExceptCardExist:
            self.input_counter -= 1
            except_dialog = TexceptionDialog(Poker_Exceptions.ExceptCardExist.__str__(Poker_Exceptions.ExceptCardExist))
            except_dialog.exec()
        except Poker_Exceptions.ExceptInvalidCardLenght:
            self.input_counter -= 1
            if self.input.text() == '':
                pass
            else:
                except_dialog = TexceptionDialog(Poker_Exceptions.ExceptInvalidCardLenght.__str__(Poker_Exceptions.ExceptInvalidCardLenght))
                except_dialog.exec()
        except Poker_Exceptions.ExceptInvalidCard:
            self.input_counter -= 1
            except_dialog = TexceptionDialog(Poker_Exceptions.ExceptInvalidCard.__str__(Poker_Exceptions.ExceptInvalidCard))
            except_dialog.exec()
        except:
            self.input_counter -= 1
            raise Exception

        self.input.clear()
        self.input.setPlaceholderText(f'Insert your {self.input_dict[self.input_counter]} card (e.g. jh)')

        if self.input_counter == 7:
            self.input.close()

    def restartMethod(self):
        self.input.clear()
        self.input_counter = int(0)
        self.clickMethod()
        self.w.close()
        self.w = None

    def showCardsMethod(self):
        # if self.w is None:
        if self.input_counter >= 2:

            self.w = TsubWindow()
            self.w.setWindowTitle('Hand Analysis')
            layout = QVBoxLayout()

            title = QLabel(f'{"":60s}{"Current Hand":30s}{"Pocket":25s}{"Table":25s}')
            cards = QLabel(f'{Poker_HandCheck.what_do_I_have(self.hand)[0]:35s}')


            if self.input_counter >= 2 and self.input_counter < 5:
                subtitle = QLabel(f'\nThe probabilities of improving your hand in the flop are:\n\n{"":33s}'
                                  f'{"Probability":20s}\t{"Odds":10s}')
                pair = QLabel(f'{"Pair: ":33s}{Poker_PreFlopOdds.pair_preflop(self.hand.pocket):<10.3%}\t\t{"1:"}'
                              f'{(1/Poker_PreFlopOdds.pair_preflop(self.hand.pocket)) - 1:<.2f}')
                dpair = QLabel(f'{"Double Pair: ":33s}{Poker_PreFlopOdds.dpair_preflop(self.hand.pocket):<10.3%}\t\t{"1:"}'
                               f'{(1 / Poker_PreFlopOdds.dpair_preflop(self.hand.pocket)) - 1:<.2f}')
                three = QLabel(f'{"Three of a kind:":33s}{Poker_PreFlopOdds.three_preflop(self.hand.pocket):<10.3%}\t\t{"1:"}'
                               f'{(1 / Poker_PreFlopOdds.three_preflop(self.hand.pocket)) - 1:<.2f}')
                straight = QLabel(f'{"Straight:":33s}{Poker_PreFlopOdds.straight_preflop(self.hand.pocket):<10.3%}\t\t{"1:"}'
                                  f'{(1 / Poker_PreFlopOdds.straight_preflop(self.hand.pocket)) - 1:<.2f}')
                flush = QLabel(f'{"Flush:":33s}{Poker_PreFlopOdds.flush_preflop(self.hand.pocket):<10.3%}\t\t{"1:"}'
                               f'{(1 / Poker_PreFlopOdds.flush_preflop(self.hand.pocket)) - 1:<.2f}')
                full = QLabel(f'{"Full house:":33s}{Poker_PreFlopOdds.full_preflop(self.hand.pocket):<10.3%}\t\t{"1:"}'
                              f'{(1 / Poker_PreFlopOdds.full_preflop(self.hand.pocket)) - 1:<.2f}')
                four = QLabel(f'{"Four of a kind:":33s}{Poker_PreFlopOdds.four_preflop(self.hand.pocket):<10.3%}\t\t{"1:"}'
                              f'{(1 / Poker_PreFlopOdds.four_preflop(self.hand.pocket)) - 1:<.0f}')
                str_flush = QLabel(f'{"Straight flush:":33s}{Poker_PreFlopOdds.straightflush_preflop(self.hand.pocket):<10.3%}\t\t{"1:"}'
                                   f'{(1 / Poker_PreFlopOdds.straightflush_preflop(self.hand.pocket)) - 1:<.2f}')
                royal = QLabel(f'{"Royal flush:":33s}{Poker_PreFlopOdds.royalflush_preflop(self.hand.pocket):<10.3%}\t\t{"1:"}'
                               f'{(1 / Poker_PreFlopOdds.royalflush_preflop(self.hand.pocket)) - 1:<.2f}')

            if self.input_counter == 5:
                subtitle = QLabel(
                    f'\nThe probabilities of improving your hand in the turn are:\n\n{"":33s}{"Probability":20s}\t{"Odds":10s}')
                pair = QLabel(
                    f'{"Pair: ":33s}{Poker_FlopOdds.pair_flop():<10.3%}\t\t{"1:"}{(1 / Poker_FlopOdds.pair_flop()) - 1:<.2f}')
                dpair = QLabel(
                    f'{"Double Pair: ":33s}{Poker_FlopOdds.dpair_flop():<10.3%}\t\t{"1:"}{(1 / Poker_FlopOdds.dpair_flop()) - 1:<.2f}')
                three = QLabel(
                    f'{"Three of a kind:":33s}{Poker_FlopOdds.three_flop():<10.3%}\t\t{"1:"}{(1 / Poker_FlopOdds.three_flop()) - 1:<.2f}')
                straight = QLabel(
                    f'{"Straight:":33s}{Poker_FlopOdds.straight_flop():<10.3%}\t\t{"1:"}{(1 / Poker_FlopOdds.straight_flop()) - 1:<.2f}')
                flush = QLabel(
                    f'{"Flush:":33s}{Poker_FlopOdds.flush_flop():<10.3%}\t\t{"1:"}{(1 / Poker_FlopOdds.flush_flop()) - 1:<.2f}')
                full = QLabel(
                    f'{"Full house:":33s}{Poker_FlopOdds.full_flop():<10.3%}\t\t{"1:"}{(1 / Poker_FlopOdds.full_flop()) - 1:<.2f}')
                four = QLabel(
                    f'{"Four of a kind:":33s}{Poker_FlopOdds.four_flop():<10.3%}\t\t{"1:"}{(1 / Poker_FlopOdds.four_flop()) - 1:<.0f}')
                str_flush = QLabel(
                    f'{"Straight flush:":33s}{Poker_FlopOdds.strflush_flop():<10.3%}\t\t{"1:"}{(1 / Poker_FlopOdds.strflush_flop()) - 1:<.2f}')
                royal = QLabel(
                    f'{"Royal flush:":33s}{Poker_FlopOdds.royalflush_flop():<10.3%}\t\t{"1:"}{(1 / Poker_FlopOdds.royalflush_flop()) - 1:<.2f}')

            if self.input_counter == 6:
                subtitle = QLabel(
                    f'\nThe probabilities of improving your hand in the river are:\n\n{"":33s}{"Probability":20s}\t{"Odds":10s}')
                pair = QLabel(
                    f'{"Pair: ":33s}{Poker_TurnOdds.pair_turn():<10.3%}\t\t{"1:"}{(1 / Poker_TurnOdds.pair_turn()) - 1:<.2f}')
                dpair = QLabel(
                    f'{"Double Pair: ":33s}{Poker_TurnOdds.dpair_turn():<10.3%}\t\t{"1:"}{(1 / Poker_TurnOdds.dpair_turn()) - 1:<.2f}')
                three = QLabel(
                    f'{"Three of a kind:":33s}{Poker_TurnOdds.three_turn():<10.3%}\t\t{"1:"}{(1 / Poker_TurnOdds.three_turn()) - 1:<.2f}')
                straight = QLabel(
                    f'{"Straight:":33s}{Poker_TurnOdds.straight_turn():<10.3%}\t\t{"1:"}{(1 / Poker_TurnOdds.straight_turn()) - 1:<.2f}')
                flush = QLabel(
                    f'{"Flush:":33s}{Poker_TurnOdds.flush_turn():<10.3%}\t\t{"1:"}{(1 / Poker_TurnOdds.flush_turn()) - 1:<.2f}')
                full = QLabel(
                    f'{"Full house:":33s}{Poker_TurnOdds.full_turn():<10.3%}\t\t{"1:"}{(1 / Poker_TurnOdds.full_turn()) - 1:<.2f}')
                four = QLabel(
                    f'{"Four of a kind:":33s}{Poker_TurnOdds.four_turn():<10.3%}\t\t{"1:"}{(1 / Poker_TurnOdds.four_turn()) - 1:<.0f}')
                str_flush = QLabel(
                    f'{"Straight flush:":33s}{Poker_TurnOdds.strflush_turn():<10.3%}\t\t{"1:"}{(1 / Poker_TurnOdds.strflush_turn()) - 1:<.2f}')
                royal = QLabel(
                    f'{"Royal flush:":33s}{Poker_TurnOdds.royalflush_turn():<10.3%}\t\t{"1:"}{(1 / Poker_TurnOdds.royalflush_turn()) - 1:<.2f}')

            title.setFont(QFont("Segoe UI", 11))
            title.setAlignment(Qt.AlignLeft)
            cards.setFont(QFont("Segoe UI", 11))
            cards.setAlignment(Qt.AlignTop)
            layout.setAlignment(Qt.AlignTop)
            layout.addWidget(title)
            layout.addWidget(cards)
            if self.input_counter < 7:
                subtitle.setAlignment(Qt.AlignLeft)
                subtitle.setFont(QFont("Segoe UI", 11, weight=QFont.Bold))
                layout.addWidget(subtitle)
                pair.setAlignment(Qt.AlignLeft)
                pair.setFont(QFont("Segoe UI", 11))
                layout.addWidget(pair)
                dpair.setAlignment(Qt.AlignLeft)
                dpair.setFont(QFont("Segoe UI", 11))
                layout.addWidget(dpair)
                three.setAlignment(Qt.AlignLeft)
                three.setFont(QFont("Segoe UI", 11))
                layout.addWidget(three)
                straight.setAlignment(Qt.AlignLeft)
                straight.setFont(QFont("Segoe UI", 11))
                layout.addWidget(straight)
                flush.setAlignment(Qt.AlignLeft)
                flush.setFont(QFont("Segoe UI", 11))
                layout.addWidget(flush)
                full.setAlignment(Qt.AlignLeft)
                full.setFont(QFont("Segoe UI", 11))
                layout.addWidget(full)
                four.setAlignment(Qt.AlignLeft)
                four.setFont(QFont("Segoe UI", 11))
                layout.addWidget(four)
                str_flush.setAlignment(Qt.AlignLeft)
                str_flush.setFont(QFont("Segoe UI", 11))
                layout.addWidget(str_flush)
                royal.setAlignment(Qt.AlignLeft)
                royal.setFont(QFont("Segoe UI", 11))
                layout.addWidget(royal)

            self.w.setLayout(layout)
            self.w.show()


def startWindow():
    app = QApplication(sys.argv)
    win = TmainWindow()
    win.show()
    sys.exit(app.exec_())

