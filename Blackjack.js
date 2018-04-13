class Blackjack {
  constructor(num_decks, hit_soft_17 = true) {
    this._suits = ["♣", "♦", "♥", "♠"];
    this._cards = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"];
    this.deck = this._create_decks(num_decks);
    
    this.player_hand = {
		  cards: [],
		  value: 0
	  };
    this.dealer_hand = {
		  cards: [],
		  value: 0
	  };
	  
	this.draw("p", 2);
    this.draw("d", 2);
    
    this._game_over = 0;
    this.hit_soft_17 = hit_soft_17;
  }
  
  hit(){
    this.draw();
    if (this.player_hand.value > 21) {
      this._game_over = 1;
      return `${this._get_hand()}: Bust! Game over. :(`;
    } else {
      return this.print_hand();
    }
  }
  
  stand(){
    // Sanity check, shouldn't happen
    this._game_over = 1;
    if (this.player_hand.value > 21) {
      return `${this._get_hand()}: Bust! Game over. :(`;
    }
	
	// If the player got a blackjack, 
	// TODO: Make this into a static method that accepts a hand
	if (this.player_hand.value === 21 && 
		this.player_hand.length === 2) {
		
		// If the dealer also got blackjack, stalemate.
		// otherwise, the player wins a modified bet
	}
    
    while (this.player_hand.value > this.dealer_hand.value || 
           this.dealer_hand.value < 17 ||
           this._is_soft() && this.hit_soft_17) {
      this.draw("d");
      if (this.dealer_hand.value > 21) {
        this._game_over = 1;
        return `${this._get_hand("d")}: House Bust! You win!`;
      }
    }
    
    // TODO: Make a game win check function already...
    // TODO: Add a check whether a person has blackjack or simply 21
    //    Blackjack always wins in this case
    if (this.calcHand() > this.calcHand("d")) {
      return `${this._get_hand()}: You win!`;
    } else {
      return `${this._get_hand()}: You lose!`;
    }
  }
  
  _create_decks(num_decks = 1) {
    let d = [],
        r = [];
    for (let s = 0; s < this._suits.length; s++) {
      for (let c = 0; c < this._cards.length; c++) {
        d.push(new Card(this._suits[s], this._cards[c]));
      }
    }
    // I could nest the for-loop yet again, but this is faster
    // and it also looks a little cleaner to me.
    for (let n = 0; n < num_decks; n++) {
      r = r.concat(d);
    }
    return r;
  }
  
  _is_soft(){
    return this.dealer_hand.cards.map(function(c){
      return (c.value === "A" ? 1: 0);
    }).reduce(function(sum, val){return sum + val;}, 0) === 1;
  }
  
  draw(target = "player", num_cards = 1) {
    let choice, card;
    for (let i = 0; i < num_cards; i++) {
      choice = this._randInt(0, this.deck.length - 1);
      card = this.deck.splice(choice, 1)[0];
      if (target === "player" || target === "p"){
        this.player_hand.cards.push(card);
      } else {
        this.dealer_hand.cards.push(card);
      }
    }
	
	if (target === "player" || target === "p"){
		this.player_hand.value = this.calcHand();
	} else {
		this.dealer_hand.value = this.calcHand("d");
	}
  }
  
  calcHand(target = "player") {
    "Returns the value of the hand based on Blackjack rules";
    let hand,
        result = 0;
    
    if (target === "player" || target === "p"){
      hand = this.player_hand.cards;
    } else {
      hand = this.dealer_hand.cards;
    }
    
    hand.sort(function(a, b){return a.value === 'A';});
    
    for (var c = 0; c < hand.length; c++) {
      if (isNaN(hand[c].value)) {
        if (hand[c].value === "A") {
          result += (result < 11 ? 11: 1);
        } else {
          result += 10;
        }
      } else {
        result += Number(hand[c].value);
      }
    }
    return result;
  }
  
  print_hand() {
    return `${this._get_hand()} (${this.player_hand.value}) House: ${this._get_hand("d").split(' ')[0]} ? - (Hit or Stand?)`;
  }
  
  _get_hand(target = "player") {
    return (['player', 'p'].includes(target) ? this.player_hand.cards: this.dealer_hand.cards)
      .map(function(c){
        return c.suit + c.value;
      }).join(' ');
  }
  
  _randInt(min, max){
    "Generates random integer between min max INCLUSIVE";
    min = Math.ceil(min);
    return Math.floor(Math.random() * (Math.floor(max) - min + 1)) + min;
  }
}

class Card {
  constructor(suit, num) {
    this.suit = suit;
    this.value = num;
  }
}


if (require.main === module) {
	var g = new Blackjack(4);

	while (g.player_hand.value < 21) {
	  console.log(g.hit());
	}

	if (g.player_hand.value < 22) {
	  console.log(g.stand());
	}
}
