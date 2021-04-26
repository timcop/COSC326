package forsale;

import java.util.List;

/**
 * Represents the state of the game when an auction is underway 
 * as needed by a strategy. 
 * 
 * @author Michael Albert
 */
public class AuctionState {
    
    private final List<PlayerRecord> players;
    private final List<PlayerRecord> playersInAuction;
    private final List<Card> cardsInAuction;
    private final List<Card> cardsInDeck;
    private final int currentBid;

    public AuctionState(List<PlayerRecord> players, List<PlayerRecord> playersInAuction, List<Card> cardsInAuction, List<Card> cardsInDeck, int currentBid) {
        this.players = players;
        this.playersInAuction = playersInAuction;
        this.cardsInAuction = cardsInAuction;
        this.cardsInDeck = cardsInDeck;
        this.currentBid = currentBid;
    }

    /**
     * 
     * @return the current bid in the auction. 
     */
    public int getCurrentBid() {
        return currentBid;
    }

    /**
     * 
     * @return The records for all the players in the game.
     */
    public List<PlayerRecord> getPlayers() {
        return players;
    }

    /**
     * 
     * @return The records for the players remaining in the auction.
     */
    public List<PlayerRecord> getPlayersInAuction() {
        return playersInAuction;
    }

    /**
     * 
     * @return The cards remaining to be auctioned in this round.
     */
    public List<Card> getCardsInAuction() {
        return cardsInAuction;
    }

    /**
     * 
     * @return The cards remaining in the deck.
     */
    public List<Card> getCardsInDeck() {
        return cardsInDeck;
    }
    
    
    
}
