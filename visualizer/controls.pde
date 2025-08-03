// controls.pde

void keyPressed() {
  // Only allow a new move if no move is currently animating OR if currentMove is null
  if (currentMove == null || currentMove.finished()) {
    applyMove(key);
  }
  // The spacebar logic for restarting currentMove might not be needed now,
  // or could be repurposed (e.g., for a scramble).
  // if (key == ' ') {
  // currentMove.start();
  // counter = 0;
  // }
}

void applyMove(char moveChar) {
  int x = 0, y = 0, z = 0; // Axis of rotation (only one will be non-zero)
  int dir = 0;             // Direction (1 for clockwise, -1 for counter-clockwise/prime)

  switch (moveChar) {
    // Front Face
    case 'f': // F (Clockwise)
      z = 1; dir = -1;
      break;
    case 'F': // F' (Counter-Clockwise / Prime)
      z = 1; dir = 1;
      break;
    // Back Face
    case 'b': // B (Clockwise)
      z = -1; dir = 1;
      break;
    case 'B': // B' (Counter-Clockwise / Prime)
      z = -1; dir = -1;
      break;
    // Up Face
    case 'u': // U (Clockwise)
       // Note: PeasyCam might invert Y, or visual interpretation.
      x = -1; dir = 1;                // The original code had y=1 for U, so let's stick to it.
                      // The actual rotation in draw() uses -currentMove.angle for Y.
      break;
    case 'U': // U' (Counter-Clockwise / Prime)
      x = -1; dir = -1;
      break;
    // Down Face
    case 'd': // D (Clockwise)
      x = 1; dir = -1;
      break;
    case 'D': // D' (Counter-Clockwise / Prime)
      x = 1; dir = 1;
      break;
    // Left Face
    case 'l': // L (Clockwise)
      y = 1; dir = 1;
      break;
    case 'L': // L' (Counter-Clockwise / Prime)
      y = 1; dir = -1;
      break;
    // Right Face
    case 'r': // R (Clockwise)
      y = -1; dir = -1;
      break;
    case 'R': // R' (Counter-Clockwise / Prime)
      y = -1; dir = 1;
      break;
    
    default:
      // Not a recognized move key
      return;
  }

  // If a valid move was identified, create and start it
  if (dir != 0) { // dir will be 0 if no case matched
    currentMove = new Move(x, y, z, dir);
    currentMove.start();
  }
}
