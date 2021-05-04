package forsale;

import forsale.strategies.*;

import java.util.ArrayList;
import java.util.List;

/**
 *
 * @author Michael Albert
 */
public class Test {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {

        List<Player> players = new ArrayList<>();
       for(int i = 0; i < 2; i++) {
           players.add(new Player("R"+ ((char) ('A' + i)), new RandomStrategy()));
       }
       players.add(new Player("Strat1", new Strat1()));
       players.add(new Player("Strat2", new Strat2()));
       players.add(new Player("Null", new NullStrategy()));
        java.util.Collections.shuffle(players);
        GameManager g = new GameManager(players);
        g.run();
        System.out.println(g);
    }

}
