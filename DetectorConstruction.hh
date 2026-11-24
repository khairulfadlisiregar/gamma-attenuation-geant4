#ifndef DetectorConstruction_h
#define DetectorConstruction_h 1

#include "G4VUserDetectorConstruction.hh"
#include "G4GenericMessenger.hh"
#include "G4LogicalVolume.hh"
#include "G4VPhysicalVolume.hh"
#include "G4Material.hh"
#include "G4SystemOfUnits.hh"
#include "globals.hh"

class DetectorConstruction : public G4VUserDetectorConstruction {
public:
  DetectorConstruction();
  ~DetectorConstruction() override;

  G4VPhysicalVolume* Construct() override;

  void SetSlabMaterial(const G4String& matName);
  void SetSlabThickness(G4double thickness);

  G4LogicalVolume* GetSlabLogicalVolume() const { return fSlabLV; }
  G4double GetSlabThickness() const { return fSlabThickness; }
  G4String GetSlabMaterialName() const { return fSlabMaterialName; }

private:
  void DefineCommands();

  G4GenericMessenger* fMessenger = nullptr;

  G4LogicalVolume* fWorldLV = nullptr;
  G4LogicalVolume* fSlabLV  = nullptr;
  G4VPhysicalVolume* fSlabPV = nullptr;

  G4Material* fWorldMat = nullptr;
  G4Material* fAlMat    = nullptr;
  G4Material* fFeMat    = nullptr;
  G4Material* fPbMat    = nullptr;

  G4String fSlabMaterialName = "G4_Pb";
  G4double fSlabThickness    = 5.0 * cm;
};

#endif
