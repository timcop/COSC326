package forsale;

import java.util.List;

/**
 * The state of a "For sale" game when players are selling to the bank.
 * 
 * @author Michael Albert
 */
public class SaleState {

    private List<PlayerRecord> players;
    private List<Integer> chequesAvailable;
    private List<Integer> chequesRemaining;

    public SaleState(List<PlayerRecord> players, List<Integer> chequesAvailable, List<Integer> chequesRemaining) {
        this.players = players;
        this.chequesAvailable = chequesAvailable;
        this.chequesRemaining = chequesRemaining;
    }

    /**
     * 
     * @return The records for the players involved in the current sale.
     */
    public List<PlayerRecord> getPlayers() {
        return players;
    }

    /**
     * 
     * @return The cheques available in the current sale.
     */
    public List<Integer> getChequesAvailable() {
        return chequesAvailable;
    }

    /**
     * 
     * @return The cheques remaining to be sold in future sales.
     */
    public List<Integer> getChequesRemaining() {
        return chequesRemaining;
    }
    
}
