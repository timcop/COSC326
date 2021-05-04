package forsale.strategies;
import forsale.*;
import java.util.*;

// A null strategy - never bid, always play your top card.
public class NullStrategy implements Strategy {
    public int bid(PlayerRecord p, AuctionState a) {
        return -1;
    }

    public Card chooseCard(PlayerRecord p, SaleState s) {
        return p.getCards().get(0);
    }
}
