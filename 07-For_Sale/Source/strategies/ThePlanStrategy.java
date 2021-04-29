package forsale.strategies;
import forsale.*;
import java.util.*;

// Our Strategy.
// .
public class ThePlanStrategy implements Strategy {
    public int bid(PlayerRecord p, AuctionState a) {
      //Always bid an even number. - but only if you plan to pull out later.
      // This maximises your returns on your bet.

        return (int) (1 + (Math.random()*p.getCash()));
    }

    public Card chooseCard(PlayerRecord p, SaleState s) {
        return p.getCards().get((int) (Math.random()*p.getCards().size()));
    }
}
