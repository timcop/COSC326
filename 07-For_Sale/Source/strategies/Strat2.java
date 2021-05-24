package forsale.strategies;
import forsale.*;
import java.util.*;

/** Strat 2.
 * Team Name: We Ballin', Wii Bowlin'.
 * Team Members: Ethan Fraser, Magdeline Huang, Jordan Kettles, Tim Copland.
 * Date: Tuesday 18 May 2021.
 * Strat 2's bidding strategy is to always bid to an even number up until half
 * it's pot  before pulling out. This maximises it's returns if it does not win
 * the round.
 * Strat 2's selling strategy is to calculate the standard deviation of the
 * cards on the table to choose whether to play a high card or a low card using
 * set hardcoded values based on the table's std deviation.
 */
public class Strat2 implements Strategy {

  private static double upper_bound = 0;

  /** Strat 2's bidding strategy is to always bid to an even number up until half
   * it's pot  before pulling out. This maximises it's returns if it does not win
   * the round.
   */
  public int bid(PlayerRecord p, AuctionState a) {
    int maxBet = (int) Math.round(p.getCash()* 0.4);
    if (a.getCurrentBid() % 2 == 0 && a.getCurrentBid() + 2 <= maxBet) {
      return (a.getCurrentBid() + 2);
    }
    else if (a.getCurrentBid() + 1 <= maxBet) {
      return (a.getCurrentBid() + 1);
    }
    return -1;
  }

  /** Strat 2's chooseCard strategy is to calculate the standard deviation of
   * of the cards on the table to choose whether to play high or low.
   */
  public Card chooseCard(PlayerRecord p, SaleState s) {
    List<Card> cards = p.getCards();
    int card_length = cards.size();
    if (card_length != 0) {
        cards.sort(Comparator.comparing(Card::getQuality));
    }
    //Calcuate the standard deviation.
    double stddeviation = 0;
    long mean = 0;
    int num_players = s.getPlayers().size();
    for(int cheque : s.getChequesAvailable()) {
      mean += cheque;
    }
    mean /= s.getChequesAvailable().size();
    for(int cheque : s.getChequesAvailable()) {
      stddeviation += Math.pow((cheque-mean), 2);
    }
    stddeviation /= s.getChequesAvailable().size();
    stddeviation = Math.sqrt(stddeviation);
    if (num_players <= 3) {
      upper_bound = 0.5;
    }
    if (stddeviation < 1.0 - upper_bound) {
      return p.getCards().get(p.getCards().size()-1);
    } else if (stddeviation <= 3.5 - upper_bound) {
      //go for the top 4 cards.
      return p.getCards().get(Math.round(p.getCards().size() * (3/num_players)));
    } else if (stddeviation <= 5.5 - upper_bound) {
      //top 3 cards
      return p.getCards().get(Math.round(p.getCards().size() * (2/num_players)));
    } else {
      //top 2 cards.
      return p.getCards().get(Math.round(p.getCards().size() * (1/num_players)));
    }
  }
}
