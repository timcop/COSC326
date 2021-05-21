package forsale.strategies;
import forsale.*;
import java.util.*;

/** Strat 3.
 * Team Name: We Ballin', Wii Bowlin'.
 * Team Members: Ethan Fraser, Magdeline Huang, Jordan Kettles, Tim Copland.
 * Date: Tuesday 18 May 2021.
 * Strat 3's bidding strategy is to...
 * Strat 3's selling strategy is to choose a card proportional to the standard
 * deviation of the cards. I.e. if the standard deviation is high, choose a high
 * value card. There is one constant value (Tim’s constant) with which various
 * computations are performed to compare the standard deviations against when
 * deciding which card to choose.
 */
public class Strat3 implements Strategy {

  private static final int NUM_OF_CARDS = 30;
  private static final double TIMS_CONSTANT = 2.2;
  private static final double[] MIN_STD_DEV = new double[]{0, Math.sqrt(2/9), Math.sqrt(1/4), Math.sqrt(3/5), Math.sqrt(2/3)};
  private static final double[] MAX_STD_DEV = new double[]{7.5, Math.sqrt(50), 7.5, Math.sqrt(51.76), Math.sqrt(51.58)};

  /** Strat 3's bidding strategy is to bid proportional to the standard
   * deviation of the bids. I.e. if the standard deviation is high, make
   * a high bid.
   */
  public int bid(PlayerRecord p, AuctionState a) {
    /* @ Tim Copland */
    /* You can just bid lower than the current bid and the game manager will
     * force you to pull out automatically.
     */
  }

  /** Strat 3's chooseCard strategy is to choose a card proportional to the
   * standard deviation of the cards. I.e. if the standard deviation is high,
   * choose a high value card. There is one constant value (Tim’s constant)
   * with which various computations are performed to compare the standard
   * deviations against when deciding which card to choose. If the standard
   * deviation doesn't meet any of the conditions, the agent plays a random
   * card.
   */
  public Card chooseCard(PlayerRecord p, SaleState s) {
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
