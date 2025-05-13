package main

import "fmt"

type person struct {
	firstName string
	lastName  string
}

func main() {
	//alex := person{firstName: "alex", lastName: "anderson"}
	//fmt.Println(alex)

	var alex person
	alex.firstName = "alex"
	alex.lastName = "anderson"
	fmt.Println(alex)
	fmt.Printf("%+v", alex)

}
