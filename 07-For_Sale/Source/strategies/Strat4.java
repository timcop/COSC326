package forsale.strategies;
import forsale.*;
import java.util.*;

/** Strat 4.
 * Team Name: We Ballin', Wii Bowlin'.
 * Team Members: Ethan Fraser, Magdeline Huang, Jordan Kettles, Tim Copland.
 * Date: Tuesday 18 May 2021.
 * Strat 4's bidding strategy is to bud in relation to the median value of the
 * property cards. On our turn, if the median property card is still on the
 * table and it is the lowest card, then pass. Otherwise, bid +1 the
 * current bid.
 * Strat 4's selling strategy is to choose a card proportional to the standard
 * deviation of the cards. I.e. if the standard deviation is high, choose a high
 * value card. There is one constant value (Tim’s constant) with which various
 * computations are performed to compare the standard deviations against when
 * deciding which card to choose.
*/
public class Strat4 implements Strategy {
  private static final int NUM_OF_CARDS = 30;
  private static final double TIMS_CONSTANT = 2.2;
  private static final double[] MIN_STD_DEV = new double[]{0, Math.sqrt(2/9), Math.sqrt(1/4), Math.sqrt(3/5), Math.sqrt(2/3)};
  private static final double[] MAX_STD_DEV = new double[]{7.5, Math.sqrt(50), 7.5, Math.sqrt(51.76), Math.sqrt(51.58)};

  private int prevCardsInDeck = 31;
  private int medianIdx;
  private Card medianCard;

  /**
    * Strat4's bidding strategy is to go for the median card on each round.
    * At the start of every round, find out what the median card is and keep
    * track of it. On each turn, check that that card is still on the table,
    * and if it is, increase your bid by one. If the median card is either
    * not on the table, or is the lowest value card on the table, then drop
    * out, taking the lowest card knowing that it is at least the value of the
    * median. This strategy will not work if the other players bid higher than
    * the value of your remaining money.
    */
  public int bid(PlayerRecord p, AuctionState a) {
    // If this is the first round, work out the index of the median card.
    // idx = floor(number of cards on table / 2)
    List<Card> cardsInAuction = a.getCardsInAuction();
    List<PlayerRecord> players = a.getPlayers();
    if (a.getCardsInDeck().size() < prevCardsInDeck){
        prevCardsInDeck = a.getCardsInDeck().size();
        medianIdx = (int) Math.floor(prevCardsInDeck / 2);
        medianCard = cardsInAuction.get(medianIdx);
    }
    if (cardsInAuction.indexOf(medianCard) < 1) {
        return -1;
    }
    return a.getCurrentBid() + 1;
  }

  /** Strat 4's chooseCard strategy is to choose a card proportional to the
   * standard deviation of the cards. I.e. if the standard deviation is high,
   * choose a high value card. There is one constant value (Tim’s constant)
   * with which various computations are performed to compare the standard
   * deviations against when deciding which card to choose. If the standard
   * deviation doesn't meet any of the conditions, the agent plays a random
   * card.
   */
  public Card chooseCard(PlayerRecord p, SaleState s) {
    //Calcuate the standard deviation.
    List<Card> cards = p.getCards();
    int card_length = cards.size();
    if (card_length != 0) {
        cards.sort(Comparator.comparing(Card::getQuality));
    }
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
    if (MAX_STD_DEV[num_players-2] - stddeviation <= TIMS_CONSTANT) {
      //bet your highest card.
      return p.getCards().get(0);
    }
    if (stddeviation - MIN_STD_DEV[num_players-2] <= TIMS_CONSTANT) {
      //bet your lowest card.
      return p.getCards().get(p.getCards().size()-1);
    }
    if (Math.abs(stddeviation - (MAX_STD_DEV[num_players-2] - MIN_STD_DEV[num_players-2])/2) <= TIMS_CONSTANT) {
      //bet middle card.
      return p.getCards().get( (int) p.getCards().size()/2);
    } else {
      return p.getCards().get((int) (Math.random()*p.getCards().size()));
    }
  }
}
