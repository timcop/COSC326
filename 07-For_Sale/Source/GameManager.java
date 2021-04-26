package forsale;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.TreeMap;


/**
 * The manager for a single game of "For Sale"
 *
 * @author Michael Albert
 */
public class GameManager {

    private final List<Player> players;
    private final List<Card> cardsRemaining;
    private final List<Integer> chequesRemaining;
    private static final List<Integer> CHEQUES = Arrays.asList(0, 0, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15);
    private final StringBuffer log = new StringBuffer();

    /**
     * Sets up a game from a list of players.
     *
     * @param players the players
     */
    public GameManager(List<Player> players) {
        this.players = players;
        log("Players: " + players.toString());

        for (Player p :
                this.players) {
            p.initialise(players.size());
        }

        // Prepare the deck
        cardsRemaining = prepareDeck(Arrays.asList(Card.values()));
        log("Cards in play: " + cardsRemaining);

        // Create and shuffle the cheques
        chequesRemaining = prepareDeck(CHEQUES);
        log("Cheques in play: " + chequesRemaining);

    }
    
    private <T> List<T> prepareDeck(List<T> cards){
        List<T> cardCopy = new ArrayList<>(cards);
        Collections.shuffle(cardCopy);
        int toRemove;
        switch (players.size()){
            case 3:
                toRemove = 6;
                break;
            case 4:
                toRemove = 2;
                break;
            default:
                toRemove = 0;
                break;
        }
        if (toRemove > 0) {
            cardCopy.subList(0, toRemove).clear();
        }
        return cardCopy;
    }

    /**
     * Runs the game.
     */
    public void run() {

        // Conduct the auction phase
        Player firstBidder = players.get(0);
        while (cardsRemaining.size() > 0) {
            firstBidder = conductAuction(firstBidder);
        }

        // Conduct the sales phase
        while (chequesRemaining.size() > 0) {
            conductSale();
        }

        // Tidy up and finish
        determineFinalStandings();
    }

    private Player conductAuction(Player firstBidder) {

        // Cycle players to the beginner (first bidder)
        while (players.get(0) != firstBidder) {
            players.add(players.remove(0));
        }

        //Initialize
        int currentBid = 0;
        List<Card> cardsInAuction = new ArrayList<>();
        for (int i = 0; i < players.size(); i++) {
            cardsInAuction.add(cardsRemaining.remove(0));
        }
        Collections.sort(cardsInAuction);
        log("Auction: " + cardsInAuction);
        List<Player> playersInAuction = new ArrayList<>(players);

        do {
            AuctionState a = getAuctionState(playersInAuction, cardsInAuction, cardsRemaining, currentBid);
            if (a.getPlayersInAuction().size() == 1) {
                Player winner = playersInAuction.get(0);
                Card c = cardsInAuction.remove(0);
                log(winner + " wins, getting " +c + " (" + c.getQuality() +") for " + winner.getBid());
                winner.completeWinningPurchase(c);
                // The auction winner is the first bidder in the next round (if any)
                return winner;
            }
            Player p = playersInAuction.remove(0);
            int bid = p.getStrategy().bid(new PlayerRecord(p), a);
            if (bid <= currentBid || bid > p.getCash()) {
                int price = p.getBid() - p.getBid()/2;
                Card c = cardsInAuction.remove(0);
                log(p + " drops out, getting " + c + " (" + c.getQuality() +") for " + price);
                p.completeLosingPurchase(c);
            } else {
                log(p + " bids " + bid);
                currentBid = bid;
                p.setBid(bid);
                playersInAuction.add(p);
            }
        } while (true);
    }

    private void conductSale() {
        List<Integer> chequesAvailable = new ArrayList<>();
        for (int i = 0; i < players.size(); i++) {
            chequesAvailable.add(chequesRemaining.remove(0));
        }
        Collections.sort(chequesAvailable);
        log("Conducting a sale with cheques: " + chequesAvailable);
        SaleState s = getSaleState(chequesAvailable, chequesRemaining);
        TreeMap<Card,Player> cardsPlayed = new TreeMap<>();
        for(Player p : players) {
            Card c = p.getStrategy().chooseCard(new PlayerRecord(p), s);
            // Check for invalid card, if so default to first remaining card
            if (!p.getCards().contains(c)) { 
                c = p.getCards().get(0);
            }
            cardsPlayed.put(c, p);
        }
        for(Card c : cardsPlayed.keySet()) {
            Player p = cardsPlayed.get(c);
            p.removeCard(c);
            int val = chequesAvailable.remove(0);
            log("Player " + p + " sold " + c + " (" + c.getQuality() + ") for " + val);
            p.addCash(val);
        }
    }

    private List<PlayerRecord> getPlayerRecords() {
        List<PlayerRecord> pl = new ArrayList<>();
        for (Player p : players) {
            pl.add(new PlayerRecord(p));
        }
        return pl;
    }

    private AuctionState getAuctionState(List<Player> playersInAuction, List<Card> cardsInAuction, List<Card> cardsRemaining, int currentBid) {
        List<PlayerRecord> al = new ArrayList<>();
        for (Player p : playersInAuction) {
            al.add(new PlayerRecord(p));
        }
        return new AuctionState(getPlayerRecords(), al, new ArrayList<>(cardsInAuction), new ArrayList<>(cardsRemaining), currentBid);
    }

    private SaleState getSaleState(List<Integer> chequesAvailable, List<Integer> chequesRemaining) {
        return new SaleState(getPlayerRecords(), new ArrayList<>(chequesAvailable), new ArrayList<>(chequesRemaining));
    }

    private void determineFinalStandings() {
        List<Player> ps = new ArrayList<>(players);
        ps.sort((o1, o2) -> o2.getCash() - o1.getCash());
        log("Final standings:");
        for(Player p : ps) log(p.getCash() + " " + p);
    }

    public List<PlayerRecord> getFinalStandings() {
        return getPlayerRecords();
    }

    void log(String string) {
        log.append(string);
        log.append('\n');
    }

  @Override
  public String toString() {
    return log.deleteCharAt(log.length()-1).toString();
  }
    
    

    
}
