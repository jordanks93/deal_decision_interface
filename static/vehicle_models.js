const modelsByMake = {
                "Freightliner": [
                    "Cascadia 126", "Cascadia 125", "Columbia", "Coronado", "Century", "M2 106", "M2 112", "FLD120", "FL70", "FL80"
                ],
                "Peterbilt": [
                    "579", "389", "379", "567", "386", "337", "348", "367"
                ],
                "Kenworth": [
                    "T680", "T880", "W900", "T800", "T370", "T660", "T700"
                ],
                "Volvo": [
                    "VNL 760", "VNL 860", "VNL 670", "VNL 780", "VNL 300", "VNR", "VHD"
                ],
                "International": [
                    "LT", "ProStar", "Lonestar", "Durastar", "HX", "MV", "9900i"
                ],
                "Mack": [
                    "Anthem", "Pinnacle", "Granite", "Vision", "CH613", "CXU613"
                ],
                "Western Star": [
                    "5700XE", "4900", "4700", "6900", "49X"
                ],
                "Great Dane": [
                    "Champion", "Everest", "Freedom", "AlumVan", "Reefer"
                ],
                "Utility": [
                    "4000D-X", "3000R", "Reefer", "Dry Van"
                ],
                "Wabash": [
                    "National", "ArcticLite", "DuraPlate", "Reefer"
                ],
                "Hyundai Translead": [
                    "HT Composite", "HT Thermotech", "HT Dry Van"
                ],
                "Stoughton": [
                    "Z-Plate", "PureBlue", "Dry Van", "Reefer"
                ],
                "Vanguard": [
                    "VXP", "VHD", "Reefer", "Dry Van"
                ],
                "Fontaine": [
                    "Infinity", "Revolution", "Velocity", "Renegade"
                ],
                "Transcraft": [
                    "Eagle", "Steel Deck", "Combo"
                ],
                "Trail King": [
                    "TK110HDG", "TK70HT", "TK80HT", "TK102HDG"
                ],
                "East": [
                    "Genesis", "BST", "MMX", "BST II"
                ],
                "MAC Trailer": [
                    "MACsimizer", "MAC Steel", "MAC Flatbed"
                ],
                "Reitnouer": [
                    "MaxMiser", "Big Bubba", "DropMiser"
                ],
                "Manac": [
                    "Darkwing", "UltraPlate", "Combo"
                ],
                "Benson": [
                    "Flatbed", "Drop Deck", "Combo"
                ],
                "Doepker": [
                    "Steel Super B", "Drop Deck", "Flatbed"
                ],
                "Wilson": [
                    "Roadbrute", "Pacesetter", "Commander"
                ],
                "Timpte": [
                    "Super Hopper", "Ag Hopper"
                ],
                "Strick": [
                    "Plate Van", "Sheet and Post"
                ],
                "Other": [
                    "Other"
                ]
            };

            const makeSelect = document.querySelector('select[name="vehicle_make"]');
            const modelSelect = document.getElementById('vehicle_model');

            makeSelect.addEventListener('change', function() {
                const make = this.value;
                modelSelect.innerHTML = '<option value="">Select Model</option>';
                if (modelsByMake[make]) {
                    modelsByMake[make].forEach(model => {
                        const opt = document.createElement('option');
                        opt.value = model;
                        opt.textContent = model;
                        modelSelect.appendChild(opt);
                    });
                } else if (make) {
                    // If make is not in the list, show "Other"
                    const opt = document.createElement('option');
                    opt.value = "Other";
                    opt.textContent = "Other";
                    modelSelect.appendChild(opt);
                }
            });