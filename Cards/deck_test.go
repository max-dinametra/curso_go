package main

import (
	"os"
	"testing"
)

func TestNewDeck(t *testing.T) {
	d := newDeck()

	if len(d) != 16 {
		t.Errorf("Expected deck length of 16, but got %v", len(d))
	}
	if d[0] != "Ace  of  Spades" {
		t.Errorf("expected first card to be Ace of Spades, but got %v", d[0])
	}
	if d[len(d)-1] != "Four  of  Clubs" {
		t.Errorf("Ecpected last card of four of clubs but got %v", d[len(d)-1])

	}

}

func TestSaveToDeckAndNewDeckFromFile(t *testing.T) {
	os.Remove("_decktesting")

	deck := newDeck()
	deck.saveToFile("_deckTesting")

	loadedDeck := newDeckFromFile("_deckTesting")

	if len(loadedDeck) != 16 {
		t.Errorf("expected 16 cards, got %v", len(loadedDeck))
	}
	os.Remove("_decktesting")
}

//t.Errorf("Expected deck length of 16, but got %v", len(d))ssaaaa
//prueba
//orueba 2 aaaa
