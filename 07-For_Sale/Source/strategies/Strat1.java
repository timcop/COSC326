package forsale.strategies;
import forsale.*;
import java.util.*;

// Our Strategy.
// .
public class Strat1 implements Strategy {

    private static final int NUM_OF_CARDS = 30;

    /* This strategy bids up to half our pot before pulling out. */
    public int bid(PlayerRecord p, AuctionState a) {
      int maxBet = (int) Math.round(p.getCash()* 0.4);
      if (a.getCurrentBid() + 1 <= maxBet) {
        return (a.getCurrentBid() + 1);
      }
      return -1;
      //Always bid an even number. - but only if you plan to pull out later.
      // This maximises your returns on your bet.

      //Try bet for the second best card every time.
      //Try and bet for the lowest card above the median of the remaining cards.
      //Set a threshold for betting and never bet higher than that.
    }

    public Card chooseCard(PlayerRecord p, SaleState s) {
      int toRemove;
      switch(s.getPlayers().size()) {
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
      if (s.getChequesRemaining().size() == NUM_OF_CARDS - s.getPlayers().size() - toRemove) {
        System.out.println("hello");
        // middle amount of players.
        //
        /* Calculate the std deviation of the whole thing. */
      }
      //Dont bet higher than the highest card around the table.
      //Betting proprotional to the standard deviation of the cards.
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
