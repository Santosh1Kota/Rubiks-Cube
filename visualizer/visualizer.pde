// rubiks_cube.pde
import peasy.*;
String[] moveQueue;
int moveIndex = 0;
HashMap<String, Integer> colorMap;
PeasyCam cam;

float speed = 0.05;
int dim = 3;
Cubie[] cube = new Cubie[dim*dim*dim];

Move[] allMoves = new Move[] {
  new Move(0, 1, 0, 1),
  new Move(0, 1, 0, -1),
  new Move(0, -1, 0, 1),
  new Move(0, -1, 0, -1),
  new Move(1, 0, 0, 1),
  new Move(1, 0, 0, -1),
  new Move(-1, 0, 0, 1),
  new Move(-1, 0, 0, -1),
  new Move(0, 0, 1, 1),
  new Move(0, 0, 1, -1),
  new Move(0, 0, -1, 1),
  new Move(0, 0, -1, -1)
};

Move currentMove;

void setup() {
  size(600, 600, P3D);
  cam = new PeasyCam(this, 400);

  int index = 0;
  for (int x = -1; x <= 1; x++) {
    for (int y = -1; y <= 1; y++) {
      for (int z = -1; z <= 1; z++) {
        PMatrix3D matrix = new PMatrix3D();
        matrix.translate(x, y, z);
        cube[index] = new Cubie(matrix, x, y, z);
        index++;
      }
    }
  }

  colorMap = new HashMap<String, Integer>();
  colorMap.put("RED", color(255, 0, 0));
  colorMap.put("GREEN", color(0, 255, 0));
  colorMap.put("BLUE", color(0, 0, 255));
  colorMap.put("YELLOW", color(255, 255, 0));
  colorMap.put("WHITE", color(255));
  colorMap.put("ORANGE", color(255, 165, 0));

  String[] lines = loadStrings("cube_colors.txt");
  String uLine = null, dLine = null;

  for (String line : lines) {
    if (line.startsWith("U ")) uLine = line;
    else if (line.startsWith("D ")) dLine = line;
  }

  for (String line : lines) {
    if (line.startsWith("U ")) line = dLine;
    else if (line.startsWith("D ")) line = uLine;

    String[] tokens = split(line, ' ');
    String face = tokens[0];
    String[] rawColors = subset(tokens, 1);

    // Convert to 3x3 matrix
    String[][] grid = new String[3][3];
    for (int i = 0; i < 9; i++) {
      int r = i / 3;
      int c = i % 3;
      grid[r][c] = rawColors[i];
    }   

    for (int r = 0; r < 3; r++) {
      for (int c = 0; c < 3; c++) {
        color cval = colorMap.get(grid[r][c]);
        setCubieColor(face, r * 3 + c, cval);
      }
    }
  }

  currentMove = null;
  loadMovesFromFile("controls.txt");
}

String[][] rotate180(String[][] grid) {
  String[][] result = new String[3][3];
  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
      result[i][j] = grid[2 - i][2 - j];
    }
  }
  return result;
}

void draw() {
  background(51);

  cam.beginHUD();
  fill(255);
  textSize(32);
  if (currentMove != null && currentMove.animating) {
    text("Animating...", 50, 50);
  } else {
    text("Press F,R,U,L,B,D (Shift for prime)", 50, 50);
  }
  cam.endHUD();

  rotateX(-0.5);
  rotateY(0.4);
  rotateZ(0.1);

  if (currentMove != null) currentMove.update();
  if ((currentMove == null || !currentMove.animating) && moveQueue != null && moveIndex < moveQueue.length) {
    String move = moveQueue[moveIndex++];
    if (move.length() == 0) return;
  
    char moveChar = convertMoveToken(move);
    if (moveChar != '\0') {
      key = moveChar;
      keyPressed();
    }
  }
  scale(50);
  for (int i = 0; i < cube.length; i++) {
    pushMatrix();
    if (currentMove != null && currentMove.animating) {
      if (abs(cube[i].z) > 0 && cube[i].z == currentMove.z) {
        rotateZ(currentMove.angle);
      } else if (abs(cube[i].x) > 0 && cube[i].x == currentMove.x) {
        rotateX(currentMove.angle);
      } else if (abs(cube[i].y) > 0 && cube[i].y == currentMove.y) {
        rotateY(-currentMove.angle);
      }
    }
    cube[i].show();
    popMatrix();
  }
}

void setCubieColor(String face, int index, color c) {
  int row = 2 - (index / 3);  // flipped row index
  int col = index % 3;

  int targetX = 0;
  int targetY = 0;
  int targetZ = 0;

  if (face.equals("U")) {
    targetY = 1;
    targetZ = 1 - row;
    targetX = -1 + col;
  } else if (face.equals("D")) {
    targetY = -1;
    targetZ = -1 + row;
    targetX = -1 + col;
  } else if (face.equals("F")) {
    targetZ = 1;
    targetY = 1 - row;
    targetX = -1 + col;
  } else if (face.equals("B")) {
    targetZ = -1;
    targetY = 1 - row;
    targetX = 1 - col;
  } else if (face.equals("L")) {
    targetX = -1;
    targetY = 1 - row;
    targetZ = 1 - col;
  } else if (face.equals("R")) {
    targetX = 1;
    targetY = 1 - row;
    targetZ = -1 + col;
  }

  for (Cubie cubie : cube) {
    if (cubie.x == targetX && cubie.y == targetY && cubie.z == targetZ) {
      cubie.setFaceColor(face, c);
    }
  }
}
//String[][] rotate90CW(String[][] grid) {
//  String[][] result = new String[3][3];
//  for (int i = 0; i < 3; i++) {
//    for (int j = 0; j < 3; j++) {
//      result[j][2 - i] = grid[i][j];
//    }
//  }
//  return result;
//}
//String[][] flipRows(String[][] grid) {
//  String[][] result = new String[3][3];
//  for (int row = 0; row < 3; row++) {
//    for (int col = 0; col < 3; col++) {
//      result[row][col] = grid[row][2 - col];
//    }
//  }
//  return result;
//}
void loadMovesFromFile(String filename) {
  String[] lines = loadStrings(filename);
  if (lines == null || lines.length == 0) return;
  moveQueue = splitTokens(lines[0], " ");
  moveIndex = 0;
}
char convertMoveToken(String token) {
  if (token.length() == 1) {
    return Character.toLowerCase(token.charAt(0));  // F → f
  } else if (token.length() == 2 && token.charAt(1) == '\'') {
    return Character.toUpperCase(token.charAt(0));  // F' → F
  }
  return '\0'; // invalid token
}
