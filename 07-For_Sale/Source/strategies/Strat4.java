package strategies;
import forsale.*;
import java.util.*;

/**
 * This class implements our "Strat4" strategy.
 * It involves trying to win the median-value card in the first round, and
 * using the standard deviation of the table to choose a card to play in the
 * second round.
 */
public class Strat4 implements Strategy {

    /**
     * Variables for keeping track of the median card in the current round.
     * 
     * prevCardsInDeck is used to check that a new round is being played, by
     * comparing the number of cards in the deck on each turn. If the number
     * of cards has dropped, you know that cards have been dealt from the deck
     * which indicated a new round.
     * 
     * medianIdx and medianCard are used to keep track of the median card and
     * its position so that you know when to drop out.
     */
    private int prevCardsInDeck = 31;
    private int medianIdx;
    private Card medianCard;

    /**
    * Go for the median card on each round. At the start of every round, find
    * out what the median card is and keep track of it. On each turn, check
    * that that card is still on the table, and if it is, increase your
    * bid by one. If the median card is either not on the table, or is the
    * lowest value card on the table, then drop out, taking the lowest card
    * knowing that it is at least the value of the median.
    * This strategy will not work if the other players bid higher than the value
    * of your remaining money.
    */
    public int bid(PlayerRecord p, AuctionState a) {
        // If this is the first round, work out the index of the median card.
        // idx = floor(number of cards on table / 2)
        List<Card> cardsInAuction = a.getCardsInAuction();
        List<PlayerRecord> players = a.getPlayers();
        if (a.getCardsInDeck().size() < this.prevCardsInDeck){
            this.prevCardsInDeck = a.getCardsInDeck().size();
            this.medianIdx = (int) Math.floor(prevCardsInDeck / 2);
            this.medianCard = cardsInAuction.get(this.medianIdx);
        }
        if (cardsInAuction.indexOf(this.medianCard) < 1) {
            return -1;
        }
        return a.getCurrentBid() + 1;
    }

    /**
     * Pick a card from your hand proportional to the standard deviation of the
     * cards on the table. uses fixed values to decide which card to pick:
     *  - If the stdev ≤ 3.5, choose from your top 4 cards.
     *  - If the stdev ≤ 5.5, choose from your top 3 cards.
     *  - Otherwise, choose from your top 2 cards.
     */
    public Card chooseCard(PlayerRecord p, SaleState s) {
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
