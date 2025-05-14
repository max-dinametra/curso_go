package main

import "fmt"

func main() {
	// var colors map[string] string
	//colors := make(map[string]string)
	colors := map[string]string{
		"red":   "#ff0000",
		"green": "#45b145",
		"white": "#fffff",
	}

	//colors["white"] = "#fffff"
	//delete(colors, "white")

	printMap(colors)
}

func printMap(c map[string]string) {
	for color, hex := range c {
		fmt.Println("hex code for", color, "is", hex)

	}
}
