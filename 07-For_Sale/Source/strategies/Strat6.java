package forsale.strategies;
import forsale.*;
import java.util.*;

public class Strat6 implements Strategy {

    public int bid(PlayerRecord p, AuctionState a) {
      int maxBet = (int) Math.round(p.getCash()* 0.4);
      if (a.getCurrentBid() % 2 == 0 && a.getCurrentBid() + 2 <= maxBet) {
        return (a.getCurrentBid() + 2);
      }
      else if (a.getCurrentBid() + 1 <= maxBet) {
        return (a.getCurrentBid() + 1);
      }
      return -1;
    }

    public Card chooseCard(PlayerRecord p, SaleState s) {
        List<Integer> total_cards;
        int num_players = s.getPlayers().size();
        double min_std;
        double max_std;
        double curr_std;
        List<Double> range_std;

        total_cards = s.getChequesRemaining();
        for (int cheque : s.getChequesAvailable()) {
            total_cards.add(cheque);
        }
        System.out.println(total_cards);

        max_std = maxStd(total_cards, num_players);
        min_std = minStd(total_cards, num_players);
        curr_std = calculateStd(s.getChequesAvailable());



        List<Card> myCards = p.getCards();
        myCards.sort(Comparator.comparing(Card::getQuality));
        System.out.println(myCards);

        range_std = rangeStd(min_std, max_std, myCards.size());
        System.out.println(range_std);
        System.out.println(normalRange(range_std, min_std, max_std));
        List<Double> normal_range = normalRange(range_std, min_std, max_std);

        for (int i = 0; i < myCards.size()-1; i++) {
            if (curr_std >= normal_range.get(i) && curr_std <= normal_range.get(i+1)) {
                System.out.println(myCards.get(i));
                return myCards.get(i);

            }

        }
        return myCards.get(0);
    }

    private List<Integer> sortList (List<Integer> list) {
        Collections.sort(list);
        return list;
    }

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

    private double minStd (List<Integer> list, int num_players) {
        double min_std = maxStd(list, num_players); //initialise it to the max
        double curr_std;
        int length = list.size();
        List<Integer> vals = new ArrayList<Integer>();
        list = sortList(list);

        for (int i = 0; i < length-num_players; i++) {
            vals = list.subList(i, i + num_players);
            // System.out.println(vals);
            curr_std = calculateStd(vals);
            // System.out.println(curr_std);
            if (curr_std < min_std) {
                min_std = curr_std;
            }
        }
        return min_std;
    }

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

    private List<Double> normalRange (List<Double> rangeStd, double min_std, double max_std) {
        double mean_std = (max_std+min_std)/2;
        List<Double> range = new ArrayList<Double>();
        double std = 0.2;


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
