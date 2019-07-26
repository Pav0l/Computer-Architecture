# Computer Architecture

## Project

- [Implement the LS-8 Emulator](ls8/)

## Task List: add this to the first comment of your Pull Request

### Day 1: Get `print8.ls8` running

- [ ] Inventory what is here
- [ ] Implement the `CPU` constructor
- [ ] Add RAM functions `ram_read()` and `ram_write()`
- [ ] Implement the core of `run()`
- [ ] Implement the `HLT` instruction handler
- [ ] Add the `LDI` instruction
- [ ] Add the `PRN` instruction

### Day 2: Add the ability to load files dynamically, get `mult.ls8` and `stack.ls8` running

- [ ] Un-hardcode the machine code
- [ ] Implement the `load()` function to load an `.ls8` file given the filename
      passed in as an argument
- [ ] Implement a Multiply instruction (run `mult8.ls8`)

### Day 3; Stack

- [ ] Implement the System Stack and be able to run the `stack.ls8` program

### Day 4: Get `call.ls8` running

- [ ] Implement the CALL and RET instructions
- [ ] Implement Subroutine Calls and be able to run the `call.ls8` program

### Stretch

- [ ] Add the timer interrupt to the LS-8 emulator
- [ ] Add the keyboard interrupt to the LS-8 emulator
- [ ] Write an LS-8 assembly program to draw a curved histogram on the screen

### Day 5 - Sprint Challenge: Conditional Jumps

Your finished project must include all of the following requirements:

- [ ] Add the `CMP` instruction and `equal` flag to your LS-8.

- [ ] Add the `JMP` instruction.

- [ ] Add the `JEQ` and `JNE` instructions.

[See the LS-8 spec for details](https://github.com/LambdaSchool/Computer-Architecture/blob/master/LS8-spec.md)

In your solution, it is essential that you follow best practices and produce
clean and professional results. Schedule time to review, refine, and assess your
work and perform basic professional polishing including spell-checking and
grammar-checking on your work. It is better to submit a challenge that meets MVP
than one that attempts too much and does not.

Validate your work through testing and ensure that your code operates as designed.

[Here is some code](sctest.ls8) that exercises the above instructions. It should
print:

```
1
4
5
```

## Sprint Challenge - Stretch Problems

After finishing your required elements, you can push your work further. These
goals may or may not be things you have learned in this module but they build on
the material you just studied. Time allowing, stretch your limits and see if you
can deliver on the following optional goals:

- [ ] Add the ALU operations: `AND` `OR` `XOR` `NOT` `SHL` `SHR` `MOD`
- [ ] Add an `ADDI` extension instruction to add an immediate value to a register
- [ ] Add timer interrupts
- [ ] Add keyboard interrupts

To test the ALU operations I've created new asembly instructions in

[here](https://github.com/Pav0l/Computer-Architecture/blob/master/ls8/examples/alu.ls8) that exercises the all ALU instructions. It should
print:

```
2
30
28
-11
2
40
1
```
