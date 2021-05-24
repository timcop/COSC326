package forsale.strategies;
import forsale.*;
import java.util.*;

/** Strat 3.
 * Team Name: We Ballin', Wii Bowlin'.
 * Team Members: Ethan Fraser, Magdeline Huang, Jordan Kettles, Tim Copland.
 * Date: Tuesday 18 May 2021.
 * Strat 3's bidding strategy is compare the standard deviation of the cards in
 * auction to a range of standard deviations of all cards remaining (including
 * on the table). We then set a max bid which is proportional to how large the
 * standard deviation is, so higher will give a higher max bid.
 * Strat 3's selling strategy is to choose a card proportional to the standard
 * deviation of the cards. I.e. if the standard deviation is high, choose a high
 * value card. There is one constant value (Tim’s constant) with which various
 * computations are performed to compare the standard deviations against when
 * deciding which card to choose.
 */
public class Strat3 implements Strategy {

  private static final int NUM_OF_CARDS = 30;
  private static final double TIMS_CONSTANT = 2.2;
  private static final double[] PROPERTY_MIN_STD_DEV = new double[]{0.5, Math.sqrt(0.66), Math.sqrt(1.25), Math.sqrt(1.2), Math.sqrt(2.9167)};
  private static final double[] PROPERTY_MAX_STD_DEV = new double[]{14.5, Math.sqrt(180.67), Math.sqrt(196.25), Math.sqrt(182), Math.sqrt(182.9)};
  private static final double[] MIN_STD_DEV = new double[]{0, Math.sqrt(2/9), Math.sqrt(1/4), Math.sqrt(3/5), Math.sqrt(2/3)};
  private static final double[] MAX_STD_DEV = new double[]{7.5, Math.sqrt(50), 7.5, Math.sqrt(51.76), Math.sqrt(51.58)};

  /** Strat 3's bidding strategy compares the standard deviation of the cards in
  * auction to a range of standard deviations of all cards remaining (including
  * on the table). We then set a max bid which is proportional to how large the
  * standard deviation is, so higher will give a higher max bid.
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


    if (bid < max_bid) {
      return bid + 1;
    }
    return -1;
  }

  /** Strat 3's chooseCard strategy is to choose a card proportional to the
   * standard deviation of the cards. I.e. if the standard deviation is high,
   * choose a high value card. There is one constant value (Tim’s constant)
   * with which various computations are performed to compare the standard
   * deviations against when deciding which card to choose. If the standard
   * deviation doesn't meet any of the conditions, the agent plays a random
   * card.
   */
  public Card chooseCard(PlayerRecord p, SaleState s) {
    //Calcuate the standard deviation.
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
    if (MAX_STD_DEV[num_players-2] - stddeviation <= TIMS_CONSTANT) {
      //bet your highest card.
      return p.getCards().get(0);
    }
    if (stddeviation - MIN_STD_DEV[num_players-2] <= TIMS_CONSTANT) {
      //bet your lowest card.
      return p.getCards().get(p.getCards().size()-1);
    }
    if (Math.abs(stddeviation - (MAX_STD_DEV[num_players-2] - MIN_STD_DEV[num_players-2])/2) <= TIMS_CONSTANT) {
      //bet middle card.
      return p.getCards().get( (int) p.getCards().size()/2);
    } else {
      return p.getCards().get((int) (Math.random()*p.getCards().size()));
    }
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


}
