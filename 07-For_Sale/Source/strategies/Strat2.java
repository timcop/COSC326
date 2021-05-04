package forsale.strategies;
import forsale.*;
import java.util.*;

// Our Strategy.
// .
public class Strat2 implements Strategy {
    /* This strategy bids up to half our pot before pulling out. */
    public int bid(PlayerRecord p, AuctionState a) {
      int maxBet = (int) Math.round(p.getCash()* 0.4);
      if (a.getCurrentBid() % 2 == 0 && a.getCurrentBid() + 2 <= maxBet) {
        return (a.getCurrentBid() + 2);
      }
      else if (a.getCurrentBid() + 1 <= maxBet) {
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
        return p.getCards().get((int) (Math.random()*p.getCards().size()));
    }
}
