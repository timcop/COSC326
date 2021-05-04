package forsale.strategies;
import forsale.*;
import java.util.*;

// A random strategy - make a random bid up to your amount remaining,
// choose a rand card to sell.
public class RandomStrategy implements Strategy {
    public int bid(PlayerRecord p, AuctionState a) {
        return (int) (1 + (Math.random()*p.getCash()));
    }

    public Card chooseCard(PlayerRecord p, SaleState s) {
        return p.getCards().get((int) (Math.random()*p.getCards().size()));
    }
}
