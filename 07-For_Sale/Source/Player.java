package forsale;

import java.util.ArrayList;
import java.util.List;

/**
 * A player in "For Sale". Player objects are manipulated only by the game
 * management class. Strategies are presented only with "PlayerRecord" objects
 * that represent a view of a particular player at a particular time.
 *
 * @author Michael Albert
 */
public class Player {

    private int cash;
    private List<Card> cards = new ArrayList<>();
    private final String name;
    private final Strategy strategy;
    private int bid = 0;

    public Player(String name, Strategy strategy) {
        this.name = name;
        this.strategy = strategy;
    }

    public void initialise(int numPlayers){
        switch (numPlayers){
            case 3: case 4:
                cash = 18;
                break;
            case 5: case 6:
                cash = 14;
                break;
            default:
                cash = 0;
        }
    }

    public List<Card> getCards() {
        return cards;
    }

    public String getName() {
        return name;
    }

    public int getCash() {
        return cash;
    }

    public int getBid() {
        return bid;
    }

    public void removeCard(Card card) {
        cards.remove(card);
    }

    public String statusReport() {
        return name + " has $" + (cash * 1000) + " and owns " + cards;
    }

    @Override
    public String toString() {
        return name;
    }

    public Strategy getStrategy() {
        return strategy;
    }

    public void completeWinningPurchase(Card c) {
        cash -= bid;
        cards.add(c);
        bid = 0;
    }

    public void completeLosingPurchase(Card c) {
        cash -= bid;
        cash += bid / 2;
        cards.add(c);
        bid = 0;
    }

    void setBid(int bid) {
        this.bid = bid;
    }

    void addCash(Integer cheque) {
        cash += cheque;
    }

}
