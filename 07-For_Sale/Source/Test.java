package forsale;

import forsale.strategies.*;

import java.util.ArrayList;
import java.util.List;
import java.util.*;

import java.io.*;


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
        // System.out.println(g);
        List<PlayerRecord> final_standings = g.getFinalStandings();

        final_standings.sort(Comparator.comparing(PlayerRecord::getCash));
        Collections.reverse(final_standings);
        try (FileWriter f = new FileWriter("scores.txt", true);
                BufferedWriter b = new BufferedWriter(f);
                PrintWriter p = new PrintWriter(b);) {
                for (PlayerRecord player : final_standings) {
                    p.println(player.getName() + " " + player.getCash());
                }
                p.println();
        } catch (IOException i) {
            i.printStackTrace();
        }
    }
}
