package forsale.strategies;
import forsale.*;
import java.util.*;

/** Strat 1.
 * Team Name: We Ballin', Wii Bowlin'.
 * Team Members: Ethan Fraser, Magdeline Huang, Jordan Kettles, Tim Copland.
 * Date: Tuesday 18 May 2021.
 * Strat 1's bidding strategy is to always bid by 1 up until half it's pot
 * before pulling out.
 * Strat 1's selling strategy is to calculate the standard deviation of the
 * cards on the table to choose whether to play a high card or a low card.
*/
public class Strat1 implements Strategy {

    private static final int NUM_OF_CARDS = 30;
    private static final double TIMS_CONSTANT = 1.5;
    private static final double[] MIN_STD_DEV = new double[]{0, Math.sqrt(2/9), Math.sqrt(1/4), Math.sqrt(3/5), Math.sqrt(2/3)};
    private static final double[] MAX_STD_DEV = new double[]{7.5, Math.sqrt(50), 7.5, Math.sqrt(51.76), Math.sqrt(51.58)};

    /** Strat 1's bid strategy is to always bid by 1, up until half of it's pot
     * before pulling out.
     */
    public int bid(PlayerRecord p, AuctionState a) {
      int maxBet = (int) Math.round(p.getCash()* 0.5);
      if (a.getCurrentBid() + 1 <= maxBet) {
        return (a.getCurrentBid() + 1);
      }
      return -1;
    }

    /** Strat 1's chooseCard strategy is to calculate the standard deviation of
     * of the cards on the table to choose whether to play high or low.
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
      if (num_players > 3) {
        if (stddeviation < 1.0) {
          return p.getCards().get(p.getCards().size()-1);
        } else if (stddeviation <= 3.5) {
          //go for the top 4 cards.
          return p.getCards().get(Math.round(p.getCards().size() * (3/num_players)));
        } else if (stddeviation <= 5.5) {
          //top 3 cards
          return p.getCards().get(Math.round(p.getCards().size() * (2/num_players)));
        } else {
          //top 2 cards.
          return p.getCards().get(Math.round(p.getCards().size() * (1/num_players)));
        }
      } else {
        return p.getCards().get((int) (Math.random()*p.getCards().size()));
      }
    }
}
