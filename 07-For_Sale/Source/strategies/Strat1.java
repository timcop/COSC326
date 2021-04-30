package forsale.strategies;
import forsale.*;
import java.util.*;

// Our Strategy.
// .
public class Strat1 implements Strategy {
    /* This strategy bids up to half our pot before pulling out. */
    public int bid(PlayerRecord p, AuctionState a) {
      int maxBet = (int) Math.round(p.getCash()* 0.4);
      if (a.getCurrentBid() + 1 <= maxBet) {
        return (a.getCurrentBid() + 1);
      }
      return -1;
      //Always bid an even number. - but only if you plan to pull out later.
      // This maximises your returns on your bet.

      //Try bet for the second best card every time.
      //Try and bet for the lowest card above the median of the remaining cards.
      //Set a threshold for betting and never bet higher than that.
    }

    public Card chooseCard(PlayerRecord p, SaleState s) {
      //Betting proprotional to the standard deviation of the cards.
      double stddeviation = 0;
      long mean = 0;
      for(int cheque : s.getChequesAvailable()) {
        mean += cheque;
      }
      mean /= s.getChequesAvailable().size();
      for(int cheque : s.getChequesAvailable()) {
        stddeviation += Math.pow((cheque-mean), 2);
      }
      stddeviation /= s.getChequesAvailable().size();
      stddeviation = Math.sqrt(stddeviation);

      System.out.println(stddeviation);
      return
        return p.getCards().get((int) (Math.random()*p.getCards().size()));
    }
}
