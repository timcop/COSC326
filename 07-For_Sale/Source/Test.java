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
        for(int i = 0; i < 0; i++) {
            players.add(new Player("R"+ ((char) ('A' + i)), new RandomStrategy()));
        }
        players.add(new Player("Strat6", new Strat6()));
        players.add(new Player("Strat5", new Strat5()));
        // players.add(new Player("Strat4", new Strat4()));
        players.add(new Player("Strat3", new Strat3()));
        players.add(new Player("Strat2", new Strat2()));
        players.add(new Player("Strat1", new Strat1()));
        java.util.Collections.shuffle(players);
        GameManager g = new GameManager(players);
        g.run();
        System.out.println(g);
        }

}
