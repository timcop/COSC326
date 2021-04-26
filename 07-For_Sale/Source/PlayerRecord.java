package forsale;

import java.util.ArrayList;
import java.util.List;

/**
 * A record of the current state of a player in "For Sale".
 * 
 * The player data available to a strategy in the course of a game
 * are just copies of the true information for a player, so that
 * manipulating them does not affect the actual player data. 
 *
 * @author Michael Albert
 */
public class PlayerRecord {

    private final List<Card> cards;
    private final int cash;
    private final String name;
    private final int currentBid;

    public PlayerRecord(List<Card> cards, int cash, int currentBid, String name) {
        this.cards = new ArrayList<Card>(cards);
        this.cash = cash;
        this.name = name;
        this.currentBid = currentBid;
    }

    public PlayerRecord(List<Card> cards, int cash, String name) {
        this(cards, cash, 0, name);
    }
    
    public PlayerRecord(Player p) {
        this(p.getCards(), p.getCash(), p.getBid(), p.getName());
    }

    /**
     * 
     * @return The cards held by this player at this time.
     */
    public List<Card> getCards() {
        return this.cards;
    }

    /**
     * 
     * @return The cash on hand for this player at this time.
     */
    public int getCash() {
        return cash;
    }

    /**
     * Returns this player's current bid in an auction. If the player has not
     * bid yet, the value is 0. If the player has dropped out, the value will
     * be negative.
     * 
     * @return This player's current bid.
     */
    public int getCurrentBid() {
        return currentBid;
    }

    /**
     * 
     * @return The player's name.
     */
    public String getName() {
        return name;
    }

}
