import json
import os

from sklearn import tree
from sklearn.feature_extraction import DictVectorizer

from survival.components.resource_component import ResourceComponent


class DecisionTree:
    def __init__(self):
        self.clf = None
        self.vec = None

    def build(self, depth: int):
        path = os.path.join("..", "data.txt")

        samples = list()
        results = list()

        with open(path, "r") as training_file:
            for sample in training_file:
                sample, result = self.process_input(sample)
                samples.append(sample)
                results.append(result)

        self.vec = DictVectorizer()
        self.clf = tree.DecisionTreeClassifier(max_depth=depth)
        self.clf = self.clf.fit(self.vec.fit_transform(samples).toarray(), results)
        # print(tree.export_text(self.clf, feature_names=self.vec.get_feature_names()))

    def predict_answer(self, resource: ResourceComponent):
        params = {
            "weight": resource.weight,
            "eatable": resource.eatable,
            "toughness": resource.toughness
        }
        return self.clf.predict(self.vec.transform(params).toarray())

    @staticmethod
    def process_input(line):
        data = json.loads(line.strip())
        result = data['resource']
        del data['resource']
        sample = data

        return sample, result

