// Rubiks Cube 3
// Daniel Shiffman
// https://thecodingtrain.com/CodingChallenges/142.3-rubiks-cube.html
// https://youtu.be/8U2gsbNe1Uo

class Cubie {
  PMatrix3D matrix;
  int x = 0;
  int y = 0;
  int z = 0;
  color c;
  Face[] faces = new Face[6];

  Cubie(PMatrix3D m, int x, int y, int z) {
    this.matrix = m;
    this.x = x;
    this.y = y;
    this.z = z;
    c = color(255);

    // Initialize each face with a direction and a default color
    faces[0] = new Face(new PVector(0, 0, -1), color(0, 0, 255));     // Back
    faces[1] = new Face(new PVector(0, 0, 1), color(0, 255, 0));      // Front
    faces[2] = new Face(new PVector(0, 1, 0), color(255, 255, 255));  // Up
    faces[3] = new Face(new PVector(0, -1, 0), color(255, 255, 0));   // Down
    faces[4] = new Face(new PVector(1, 0, 0), color(255, 150, 0));    // Right
    faces[5] = new Face(new PVector(-1, 0, 0), color(255, 0, 0));     // Left
  }

  void turnFacesZ(int dir) {
    for (Face f : faces) {
      f.turnZ(dir * HALF_PI); 
    }
  }

  void turnFacesY(int dir) {
    for (Face f : faces) {
      f.turnY(dir * HALF_PI); 
    }
  }

  void turnFacesX(int dir) {
    for (Face f : faces) {
      f.turnX(dir * HALF_PI); 
    }
  }

  void update(int x, int y, int z) {
    matrix.reset(); 
    matrix.translate(x, y, z);
    this.x = x;
    this.y = y;
    this.z = z;
  }

  void show() {
    noFill();
    stroke(0);
    strokeWeight(0.1);
    pushMatrix(); 
    applyMatrix(matrix);
    box(1);
    for (Face f : faces) {
      f.show();
    }
    popMatrix();
  }

  // ✅ New method to set color on a specific face by label
  void setFaceColor(String face, color c) {
    if (face.equals("B")) faces[0].c = c;
    else if (face.equals("F")) faces[1].c = c;
    else if (face.equals("U")) faces[2].c = c;
    else if (face.equals("D")) faces[3].c = c;
    else if (face.equals("R")) faces[4].c = c;
    else if (face.equals("L")) faces[5].c = c;
  }
}
