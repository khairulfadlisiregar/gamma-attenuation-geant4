#include "DetectorConstruction.hh"

#include "G4NistManager.hh"
#include "G4Box.hh"
#include "G4LogicalVolume.hh"
#include "G4PVPlacement.hh"
#include "G4RunManager.hh"
#include "G4SystemOfUnits.hh"
#include "G4VisAttributes.hh"
#include "G4Color.hh"

DetectorConstruction::DetectorConstruction() {
  DefineCommands();
}

DetectorConstruction::~DetectorConstruction() {
  delete fMessenger;
}

void DetectorConstruction::DefineCommands() {
  fMessenger = new G4GenericMessenger(this, "/attenuation/slab/",
                                      "Control slab material and thickness");

  auto& matCmd = fMessenger->DeclareMethod("material",
                                          &DetectorConstruction::SetSlabMaterial,
                                          "Set slab material (G4_Al, G4_Fe, G4_Pb)");
  matCmd.SetParameterName("mat", false);
  matCmd.SetDefaultValue("G4_Pb");
  matCmd.SetCandidates("G4_Al G4_Fe G4_Pb Al Fe Pb");

  auto& thickCmd = fMessenger->DeclareMethodWithUnit("thickness", "cm",
                                                   &DetectorConstruction::SetSlabThickness,
                                                   "Set slab thickness along Z");
  thickCmd.SetParameterName("thickness", false);
  thickCmd.SetDefaultValue("5.0");
}

G4VPhysicalVolume* DetectorConstruction::Construct() {
  auto* nist = G4NistManager::Instance();

  fWorldMat = nist->FindOrBuildMaterial("G4_AIR");
  fAlMat    = nist->FindOrBuildMaterial("G4_Al");
  fFeMat    = nist->FindOrBuildMaterial("G4_Fe");
  fPbMat    = nist->FindOrBuildMaterial("G4_Pb");

  G4double worldXY = 50.0 * cm;
  G4double worldZ  = 60.0 * cm;

  auto* worldSolid = new G4Box("World", worldXY * 0.5, worldXY * 0.5, worldZ * 0.5);
  fWorldLV = new G4LogicalVolume(worldSolid, fWorldMat, "World");
  fWorldLV->SetVisAttributes(G4VisAttributes::GetInvisible());

  auto* worldPV = new G4PVPlacement(nullptr, G4ThreeVector(), fWorldLV,
                                    "World", nullptr, false, 0, true);

  G4double slabXY = 20.0 * cm;
  auto* slabSolid = new G4Box("Slab", slabXY * 0.5, slabXY * 0.5, fSlabThickness * 0.5);

  G4Material* activeMat = fPbMat;
  if (fSlabMaterialName == "G4_Al" || fSlabMaterialName == "Al") activeMat = fAlMat;
  else if (fSlabMaterialName == "G4_Fe" || fSlabMaterialName == "Fe") activeMat = fFeMat;

  fSlabLV = new G4LogicalVolume(slabSolid, activeMat, "Slab");

  auto* slabVis = new G4VisAttributes(G4Color(0.2, 0.5, 0.9, 0.8));
  slabVis->SetForceSolid(true);
  fSlabLV->SetVisAttributes(slabVis);

  fSlabPV = new G4PVPlacement(nullptr, G4ThreeVector(0., 0., 0.), fSlabLV,
                              "Slab", fWorldLV, false, 0, true);

  return worldPV;
}

void DetectorConstruction::SetSlabMaterial(const G4String& matName) {
  fSlabMaterialName = matName;
  if (fSlabLV) {
    if (matName == "G4_Al" || matName == "Al") fSlabLV->SetMaterial(fAlMat);
    else if (matName == "G4_Fe" || matName == "Fe") fSlabLV->SetMaterial(fFeMat);
    else fSlabLV->SetMaterial(fPbMat);

    G4RunManager::GetRunManager()->GeometryHasBeenModified();
  }
}

void DetectorConstruction::SetSlabThickness(G4double thickness) {
  if (thickness <= 0.) return;
  fSlabThickness = thickness;
  if (fSlabLV) {
    auto* box = dynamic_cast<G4Box*>(fSlabLV->GetSolid());
    if (box) {
      box->SetZHalfLength(0.5 * fSlabThickness);
      G4RunManager::GetRunManager()->GeometryHasBeenModified();
    }
  }
}
