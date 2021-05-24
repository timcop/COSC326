package forsale.strategies;
import forsale.*;
import java.util.*;

/** Strat 6.
 * Team Name: We Ballin', Wii Bowlin'.
 * Team Members: Ethan Fraser, Magdeline Huang, Jordan Kettles, Tim Copland.
 * Date: Tuesday 24 May 2021.
 * Strat 6's bidding strategy is compare the standard deviation of the cards in
 * auction to a range of standard deviations of all cards remaining (including
 * on the table). We then set a max bid which is proportional to how large the
 * standard deviation is, so higher will give a higher max bid.
 * Strat 6's selling strategy is similar to the bidding strat, we compare the
 * standard deviation of the cards on the table to all the cards remaining and
 * make a range of standard deviations for which card to play. In research it
 * was found that the standard deviations possible formed a normal gaussian
 * distribution, so I wanted larger ranges for the tails of the distribution
 * and smaller closer to the mean. However for 2 players, the distribution
 * a left-skewed gaussian so I just decided to use a linear range for this case.
*/
public class Strat6 implements Strategy {

    /** Takes parameters of game state and returns a bid to perform
    * @param PlayerRecord p The players record
    * @param AuctionState a State of the auction
    *
    * @return int bid The bid to be performed
    */
    public int bid(PlayerRecord p, AuctionState a) {

        List<Card> cards_inauction = a.getCardsInAuction();
        int num_cards = cards_inauction.size();

        List<Card> total_cards = a.getCardsInDeck();
        for (Card card : a.getCardsInAuction()) {
            total_cards.add(card);
        }

        int num_players = a.getPlayers().size();
        double max_std = maxStd_cards(total_cards, num_cards);
        double min_std = minStd_cards(total_cards, num_cards);
        double mean_std = (max_std + min_std)/2;
        double curr_std = calculateStd_cards(cards_inauction);
        List<Double> range_std = rangeStd(min_std, max_std, 6);
        List<Double> normal = normalRange(range_std, min_std, max_std);

        int stack = p.getCash();
        int max_bid = stack/2;

        int turns_left = a.getCardsInDeck().size()/num_players;
        // UNCOMMENT FOR LINEAR RANGE
        // if (min_std != max_std) {
        //     for (int i = 0; i < range_std.size()-1; i++) {
        //         if (curr_std >= range_std.get(i) && curr_std <= range_std.get(i+1)) {
        //             max_bid = i*stack/6;
        //         }
        //     }
        // }

        // NORMAL RANGE
        if (min_std != max_std) {
            for (int i = 0; i < normal.size()-1; i++) {
                if (curr_std >= normal.get(i) && curr_std <= normal.get(i+1)) {
                    max_bid = i*stack/6;
                }
            }
        }
        int bid = a.getCurrentBid();

        // UNCOMMENT TO ALSO INCLUDE EVEN BIDS
        // if (bid % 2 == 0) {
        //     if (bid < max_bid -1) {
        //         return bid + 2;
        //     }
        // } else if (bid < max_bid) {
        //     return bid + 1;
        // }

        // ODD AND EVEN BIDS
        if (bid < max_bid) {
            return bid + 1;
        }
        return -1;
    }

    /** Takes parameters of game state and returns a card to play.
    * @param PlayerRecord p The players record
    * @param SaleState s The state of the current sale
    *
    * @return Card card The card to be played
    */
    public Card chooseCard(PlayerRecord p, SaleState s) {
        List<Integer> total_cards = s.getChequesRemaining();
        for (int cheque : s.getChequesAvailable()) {
            total_cards.add(cheque);
        }

        List<Card> myCards = p.getCards();
        myCards.sort(Comparator.comparing(Card::getQuality));
        int num_cards = myCards.size();

        int num_players = s.getPlayers().size();
        double min_std = minStd(total_cards, num_players);
        double max_std = maxStd(total_cards, num_players);
        double curr_std = calculateStd(s.getChequesAvailable());
        List<Double> range_std = rangeStd(min_std, max_std, myCards.size());
        List<Double> normal_range = normalRange(range_std, min_std, max_std);

        // Use just linear range
        if (num_players == 2) {
            for (int i = 0; i < myCards.size()-1; i++) {
                if (curr_std >= range_std.get(i) && curr_std <= range_std.get(i+1)) {
                    return myCards.get(i);
                }
            }
        }
        // Use normal range
        else{
            for (int i = 0; i < myCards.size()-1; i++) {
                if (curr_std >= normal_range.get(i) && curr_std <= normal_range.get(i+1)) {
                    return myCards.get(i);
                }
            }
        }
        return myCards.get(0);
    }

    // Sorts a list of type List<Integer>
    private List<Integer> sortList (List<Integer> list) {
        Collections.sort(list);
        return list;
    }

    // Calculate standard deviation for type List<Integer>
    private double calculateStd (List<Integer> vals) {
        int N = vals.size();
        double mean = 0;
        double sum = 0;
        double std = 0;

        for (double num : vals) {
            sum += num;
        }
        mean = sum/N;
        sum = 0;
        for (double num : vals) {
            sum += Math.pow(num-mean, 2);
        }
        std = sum/(N-1);
        std = Math.sqrt(std);

        return std;
    }

    // Calculate standard deviation for type List<Cards>
    private double calculateStd_cards (List<Card> cards) {
        int N = cards.size();
        double mean = 0;
        double sum = 0;
        double std = 0;

        for (Card card : cards) {
            sum += card.getQuality();
        }
        mean = sum/N;
        sum = 0;
        for (Card card : cards) {
            sum += Math.pow(card.getQuality()-mean, 2);
        }
        std = sum/(N-1);
        std = Math.sqrt(std);

        return std;
    }

    // Find the max standard deviation. Note we can do this by
    // first sorting the list then building up another list by
    // swapping between low-high values.
    private double maxStd (List<Integer> list, int num_players) {
        list = sortList(list);
        int length = list.size();
        boolean large = false;
        List<Integer> vals = new ArrayList<Integer>();

        if (length < 2) {
            return 0.0;
        }
        int count = 0;
        for (int i = 0; i < num_players; i++) {
            if (!large) {
                vals.add(list.get(count));
                large = true;
            } else {
                vals.add(list.get((length-count)-1));
                large = false;
                count++;
            }
        }
        return calculateStd(vals);
    }

    // Compute max standard deviation of list of type List<Card>
    private double maxStd_cards (List<Card> cards, int num_players) {
        cards.sort(Comparator.comparing(Card::getQuality));
        int length = cards.size();
        boolean large = false;
        List<Integer> vals = new ArrayList<Integer>();

        if (length < 2) {
            return 0.0;
        }
        int count = 0;
        for (int i = 0; i < num_players; i++) {
            if (!large) {
                vals.add(cards.get(count).getQuality());
                large = true;
            } else {
                vals.add(cards.get((length-count)-1).getQuality());
                large = false;
                count++;
            }
        }
        return calculateStd(vals);
    }

    // Compute min standard deviation, we sort the list and work through
    // taking subLists of size k = num_players. Note that the minimum standard
    // deviation will be a set of numbers closest to eachother, so this is valid.
    private double minStd (List<Integer> list, int num_players) {
        double min_std = maxStd(list, num_players); //initialise it to the max
        double curr_std;
        int length = list.size();
        List<Integer> vals = new ArrayList<Integer>();
        list = sortList(list);

        for (int i = 0; i < length-num_players; i++) {
            vals = list.subList(i, i + num_players);
            curr_std = calculateStd(vals);
            if (curr_std < min_std) {
                min_std = curr_std;
            }
        }
        return min_std;
    }

    // Compute min standard deviation with lsit type List<Card>.
    private double minStd_cards (List<Card> cards, int num_players) {
        double min_std = maxStd_cards(cards, num_players); //initialise it to the max
        double curr_std;
        int length = cards.size();
        List<Card> subCards = new ArrayList<Card>();
        cards.sort(Comparator.comparing(Card::getQuality));

        for (int i = 0; i < length-num_players; i++) {
            subCards = cards.subList(i, i + num_players);
            curr_std = calculateStd_cards(subCards);
            if (curr_std < min_std) {
                min_std = curr_std;
            }
        }
        return min_std;
    }

    // Create a linear range of standard deviation from min to max.
    private List<Double> rangeStd (double minstd, double maxstd, int num_cards) {
        double range = (maxstd-minstd);
        double range_len = num_cards+1;
        double step = range/(num_cards);
        List<Double> cards = new ArrayList<Double>();

        for (int i = 0; i < range_len; i++) {
            cards.add(minstd + i*step);
        }
        return cards;
    }

    // Create a normal range of standard deviation from min to max.
    private List<Double> normalRange (List<Double> rangeStd, double min_std, double max_std) {
        double mean_std = (max_std+min_std)/2;
        List<Double> range = new ArrayList<Double>();
        double std = 1;

        for (double x : rangeStd) {
            if (x == min_std) {
                range.add(x);
            } else if (x == max_std) {
                range.add(x);
            } else if (x < mean_std) {
                double y = 2*(x-min_std)/(max_std-min_std);
                y = -2*Math.log(y);
                y = std*Math.sqrt(y) + mean_std;
                range.add(y);
            } else {
                double y = -2*(x-max_std)/(max_std-min_std);
                y = -2*Math.log(y);
                y = -std*Math.sqrt(y) + mean_std;
                range.add(y);
            }
        }
        Collections.sort(range);
        return range;
    }
}
